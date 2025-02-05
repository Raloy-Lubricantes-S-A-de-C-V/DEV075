from django.urls import path
from . import views


urlpatterns = [

    path(
        route='',
        view=views.Principal.as_view(),
        name=''
    ),
    path(
        route='v1',
        view=views.Principal.as_view(),
        name='v1'
    ),
    path(
        route='v1/epicor01',
        view=views.Principal.as_view(),
        name='get_select_fusion'
    ),
    path(
        route='v1/epicor01/resources',
        view=views.Principal.as_view(),
        name='v1/epicor01/resources'
    ),

]