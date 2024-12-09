from django.contrib import admin

from .models import Upload

class UploadAdmin(admin.ModelAdmin):
    list_display = ["model_name", "file", "uploaded_at"]
    pass


admin.site.register(Upload, UploadAdmin)
