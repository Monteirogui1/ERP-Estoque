from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView


# PÁGINA LOGIN
# ----------------------------------------------

class ErpLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home:dashboard')
    redirect_authenticated_user = True