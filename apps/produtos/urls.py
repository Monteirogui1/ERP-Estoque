from django.urls import path
from core import settings
from django.conf.urls.static import static

from .views import ProdutoListView, ProdutoCreateView, ProdutoDetailView, ProdutoUpdateView, \
    ProdutoDeleteView

app_name = 'produtos'

urlpatterns = [
    path('Produto/', ProdutoListView.as_view(), name='produtos_list'),
    path('Produto/criar/', ProdutoCreateView.as_view(), name='produtos_form'),
    path('Produto/<int:pk>/detalhe/', ProdutoDetailView.as_view(), name='produtos_detail'),
    path('Produto/<int:pk>/atualizar/', ProdutoUpdateView.as_view(), name='produtos_form'),
    path('Produto/<int:pk>/deletar/', ProdutoDeleteView.as_view(), name='produtos_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)