from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from accounts.forms import EmailAuthenticationForm, RegistrationForm


class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:personal_area")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(DjangoLoginView):
    template_name = "accounts/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


class PersonalAreaView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/personal_area.html"
