from django.apps import apps

#| only list those that are created by the developer or owner.
def get_custom_models():
    default_models = ["ContentType", "Session", "LogEntry", "Group", "Permission", "Upload"]

    #! filtering the custom model.
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models
