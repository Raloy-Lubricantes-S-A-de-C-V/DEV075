from django.urls import path
from . import views

urlpatterns = [
    path(
        route='software/',
        view=views.SoftwareView.as_view(),
        name='software'
    ),
]