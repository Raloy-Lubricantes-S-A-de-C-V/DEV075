from django.contrib import admin
from .models import Profile
from the_applications.general_settings.models import ModelConfig, ModelBackground

admin.site.register(Profile)

admin.site.register(ModelConfig)
admin.site.register(ModelBackground)
