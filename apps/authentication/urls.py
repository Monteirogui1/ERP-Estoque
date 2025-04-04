from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views import ErpLoginView

app_name = 'authentication'

urlpatterns = [
    path('', ErpLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
]