from django.urls import path
from . import views

urlpatterns = [
    path(
        route='networks_devices/',
        view=views.RedesView.as_view(),
        name='redes'
    ),
]