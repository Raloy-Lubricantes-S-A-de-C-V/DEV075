from django.urls import path
from . import views


urlpatterns = [

    path(
        route='',
        view=views.LoginView.as_view(redirect_authenticated_user=True),
        name='login'
    ),

    # path(
    #     route='logout/',
    #     view=views.LogoutView.as_view(),
    #     name='logout'
    # ),

    path(
        route='logout/',
        view=views.logout,
        name='logout'
    ),
    path(
        route='signup/',
        view=views.SignupView.as_view(),
        name='signup'
    ),

    path(
        route='me/profile',
        view=views.update_profile,
        name="update_profile"
    ),

]