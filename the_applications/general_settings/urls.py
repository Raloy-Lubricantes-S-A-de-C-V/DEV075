from django.urls import path
from . import views


urlpatterns = [
    path(
        route='panel',
        view=views.ping,
        name='ping'
    ),

    path(
        route='dashboard',
        view=views.dashboard,
        name='dashboard'
    ),
]