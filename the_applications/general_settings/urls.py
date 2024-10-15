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

    path(
        route='getnoty',
        view=views.GetNotify.as_view(),
        name='getnoty'
    ),

    path(
        route='getnavbar',
        view=views.GetNavbar.as_view(),
        name='getnavbar'
    ),
]