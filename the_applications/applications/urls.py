from django.urls import path
from . import views

urlpatterns = [
    path(
        route='applications/',
        view=views.AplicacionesView.as_view(),
        name='aplicaciones'
    ),
]