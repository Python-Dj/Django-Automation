from django.shortcuts import render, redirect
from django.core.management import call_command
from django.conf import settings
from django.contrib import messages

from .utils import get_custom_models
from uploads.models import Upload



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

        #! Now here we call the our importdata command.
        try:
            call_command("importdata", file_path, model_name)
            messages.success(request, "Data imported Successfully!")
        except Exception as e:
            messages.error(request, str(e))

        return redirect("import-data")

    custom_models = get_custom_models()
    context = {
        "custom_models": custom_models,
    }
    return render(request, "dataentry/importdata.html", context)