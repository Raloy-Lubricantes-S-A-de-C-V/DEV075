from django.urls import path
from . import views


urlpatterns = [
    path(
        route='',
        view=views.Principal.as_view(),
        name=''
    ),
    path(
        route='datatables_info',
        view=views.DataTablesInfo.as_view(),
        name='datatables_info'
    ),
    path(
        route='showid',
        view=views.ShowId,
        name='showid'
    ),
    path(
        route='active_toggle_rules',
        view=views.DatatablesActiveToggleRules.as_view(),
        name='active_toggle_rules'
    ),
    path(
        route='delete_rules',
        view=views.DatatablesDeleteRules.as_view(),
        name='delete_rules'
    ),
    path(
        route='update_model',
        view=views.UpdateModel.as_view(),
        name='update_model'
    )
]