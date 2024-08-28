from django.urls import path
from . import views


urlpatterns = [

    path(
        route='panel',
        view=views.Principal.as_view(),
        name='panel'
    ),
    path(
        route='create_type',
        view=views.CreateTypeNotify.as_view(),
        name='create_type'
    ),
    path(
        route='create_notify',
        view=views.CreateNotify.as_view(),
        name='create_notify'
    ),
    path(
        route='datatables_type_notify',
        view=views.DatatablesTypeNotify.as_view(),
        name='datatables_type_notify'
    ),
    path(
        route='datatables_notify',
        view=views.DatatablesNotify.as_view(),
        name='datatables_notify'
    ),
    path(
        route='showid',
        view=views.ShowId,
        name='showid'
    ),

   

]