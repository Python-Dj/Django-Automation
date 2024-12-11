import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.management import call_command
from django.conf import settings
from django.contrib import messages

from .utils import get_custom_models
from uploads.models import Upload
from .task import import_data_task, export_data_task
from .utils import check_csv_errors, send_email_notification



def import_data(request):
    if request.method == "POST":
        file_path = request.FILES.get("file_path")
        model_name = request.POST.get("model_name")

        #Note: Store the file in Upload model.
        upload = Upload.objects.create(file=file_path, model_name=model_name) 
    
        #! construct full path of file.
        relative_path = upload.file.url 
        base_url = settings.BASE_DIR
        file_path = str(base_url)  +str(relative_path)

        #! check for the csv error
        try:
            check_csv_errors(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import-data')

        #| handle the impportdata task here.
        import_data_task.delay(file_path, model_name)

        messages.success(request, "Your data is being imported, you wil be notified once it is done!")

        return redirect("import-data")

    custom_models = get_custom_models()
    context = {
        "custom_models": custom_models,
    }
    return render(request, "dataentry/importdata.html", context)


def export_data(request):
    if request.method == "POST":
        model_name = request.POST.get("model_name")
        try:
            export_data_task.delay(model_name)
        except Exception as e:
            messages.error(request, str(e))
            redirect("export-data")
        messages.success(request, "Your Data is Exported!!")
        redirect("export-data")

    custom_models = get_custom_models()
    context = {
        "custom_models": custom_models
    }
    return render(request, "dataentry/exportdata.html", context)