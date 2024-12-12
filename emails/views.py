import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

from dataentry.utils import send_email_notification

from .forms import EmailForm
from .models import Email, Subscriber
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
            send_emails_task.delay(mail_subject, message, to_email, attachment)

            messages.success(request, "Email sent Successfully! ")
            redirect("send-email")
        else:
            context = {"form": form}
            return render(request, "emails/send-email.html", context)
        
    form = EmailForm()
    context = {"form": form}
    return render(request, "emails/send-email.html", context)