#django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView, ListView
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
# Model

from .models import Profile
from the_applications.general_settings.models import ModelBackground, ModelConfig


# Forms
from .forms import SignupForm ,ProfileForm

class LoginView(auth_views.LoginView):
    template_name = 'users/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = "Raloy Lubricantes"
        try:
            # context['settings'] = ModelConfig.objects.get(pk=1)
            context['settings'] = "Roadly"
            context['subsetting'] = "Ruteador"
        except:
            context['settings'] = "Roadly"
            context['subsetting'] = "Ruteador"
        context['img'] = ModelBackground.objects.all()
        self.template_name = 'users/login.html'
        return context

# class LogoutView(LoginRequiredMixin, auth_views.LoginView):
#     template_name = 'users/login.html'

def logout(request):
    # clear the user's session data
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('users:login')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['company'] = "Raloy Lubricantes"
    #     context['settings'] = "Roadly"
    #     context['img'] = ModelBackground.objects.all()
    #     context['register'] = 'Bienvenido, por favor registre sus datos'
    #     self.template_name = 'users/login.html'
    #     return context




class SignupView(FormView):
    """Users sign up view."""

    template_name = 'users/base.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = "Raloy Lubricantes"
        try:
            context['settings'] = ModelConfig.objects.get(pk=1)
        except:
            print("aqui")
            context['settings'] = "Roadly"
        context['img'] = ModelBackground.objects.all()
        context['register'] = 'Bienvenido, por favor registre sus datos'
        self.template_name = 'users/signup.html'
        return context

@login_required
def update_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            profile.phone_number = data['phone_number']
            profile.biography = data['biography']
            profile.picture = data['picture']
            profile.theme = data['theme']
            profile.save()

            return redirect('++:form')
    else:
        form = ProfileForm()

    return render(
        request=request,
        template_name='users/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form
        }
    )


