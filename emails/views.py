import os

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone

from dataentry.utils import send_email_notification

from .forms import EmailForm
from .models import Email, Subscriber, EmailTracking, Sent
from .task import send_emails_task



def send_email(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.save()

            email_list = email.email_list
            mail_subject = email.subject
            message = email.body
            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None
            subscribers = Subscriber.objects.filter(email_list=email_list)
            to_email = [sub.email_address for sub in subscribers]

            #! Handover email sending task to salary.
            send_emails_task.delay(mail_subject, message, to_email, attachment, email.id)

            messages.success(request, "Email sent Successfully! ")
            redirect("send-email")
        else:
            context = {"form": form}
            return render(request, "emails/send-email.html", context)
        
    form = EmailForm()
    context = {"form": form}
    return render(request, "emails/send-email.html", context)


def track_click(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get("url")
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except:
        return HttpResponse("Email tracking record not found!")


def track_open(request, unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse("Email open Successfully!")
        else:
            return HttpResponse("Email already Opened!")
    except:
        return HttpResponse("Email tracking record not found!")


def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum("sent__total_sent")).order_by("-sent_at")
    context = {
        "emails": emails,
    }
    return render(request, "emails/track-dashboard.html", context)


def track_stats(request, id):
    email = get_object_or_404(Email, id=id)
    sent = Sent.objects.get(email=email)
    context = {"email": email, "total_sent": sent.total_sent}
    return render(request, "emails/track-stats.html", context)