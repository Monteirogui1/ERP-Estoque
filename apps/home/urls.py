from .views import IndexTemplateView, SearchView
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'home'

urlpatterns = [
    # GET /
    path('dashboard/', IndexTemplateView.as_view(), name="dashboard"),
    path('search/', SearchView.as_view(), name='search'),
]