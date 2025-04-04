from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.authentication.urls', namespace='login')),
    path('', include('apps.home.urls',)),

    path('', include('apps.categorias.urls',)),
    path('', include('apps.fornecedor.urls',)),
    path('', include('apps.marcas.urls',)),
    path('', include('apps.produtos.urls',)),
    path('', include('apps.movimentacao.urls',)),
    path('', include('apps.notificacao.urls',)),
]
