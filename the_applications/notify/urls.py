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
    path(
        route='post_change_important',
        view=views.PostChangeImportant.as_view(),
        name='post_change_important'
    ),
    path(
        route='post_change_trash',
        view=views.PostChangeTrash.as_view(),
        name='post_change_trash'
    ),
    path(
        route='post_change_active',
        view=views.PostChangeActive.as_view(),
        name='post_change_active'
    ),
    path(
        route='inbox',
        view=views.PostChangeActive.as_view(),
        name='inbox'
    ),
    path(
        route='important',
        view=views.PostChangeActive.as_view(),
        name='important'
    ),
    path(
        route='send',
        view=views.PostChangeActive.as_view(),
        name='send'
    ),
    path(
        route='trash',
        view=views.PostChangeActive.as_view(),
        name='trash'
    ),

   

]