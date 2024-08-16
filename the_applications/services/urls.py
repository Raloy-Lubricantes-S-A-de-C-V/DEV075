from django.urls import path
from . import views

urlpatterns = [
    path(
        route='services_app/',
        view=views.ServiciosView.as_view(),
        name='servicios_app'
    ),
]