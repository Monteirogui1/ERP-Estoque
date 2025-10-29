from django.urls import path
from .views import ClienteWizardView

urlpatterns = [
    path('admin/novo-cliente/', ClienteWizardView.as_view(), name='cliente_wizard'),
]
