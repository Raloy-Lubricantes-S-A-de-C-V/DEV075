from django.urls import path
from . import views


urlpatterns = [
    path(
        route='',
        view=views.Principal.as_view(),
        name=''
    ),
    path(
        route='model',
        view=views.Modelx.as_view(),
        name='model'
    ),
    path(
        route='model2',
        view=views.Modelx2.as_view(),
        name='model2'
    ),
    path(
        route='create',
        view=views.UpdateModel.as_view(),
        name='create'
    ),
    path(
        route='update_model',
        view=views.UpdateModel.as_view(),
        name='update_model'
    ),
    path(
        route='datatables_model',
        view=views.DatatablesModel.as_view(),
        name='datatables_model'
    ),
    path(
        route='delete_rules',
        view=views.DatatablesDeleteRules.as_view(),
        name='delete_rules'
    ),
    path(
        route='active_toggle_rules',
        view=views.DatatablesActiveToggleRules.as_view(),
        name='active_toggle_rules'
    ),
    path(
        route='showid',
        view=views.ShowId,
        name='showid'
    ),
    path(
        route='get_filedsmodel_id',
        view=views.PostGetFieldsModelId.as_view(),
        name='get_filedsmodel_id'
    )
]