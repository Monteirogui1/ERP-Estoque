from django.urls import path
from .views import MovimentacaoListView, MovimentacaoCreateView, MovimentacaoDetailView, MovimentacaoDeleteView, \
    BuscarProdutoPorCodigoView

app_name = 'movimentacao'

urlpatterns = [
    path('Movimentacao/', MovimentacaoListView.as_view(), name='movimentacao_list'),
    path('Movimentacao/criar/', MovimentacaoCreateView.as_view(), name='movimentacao_create'),
    path('Movimentacao/<int:pk>/detail/', MovimentacaoDetailView.as_view(), name='movimentacao_detail'),
    path('Movimentacao/excluir/<int:pk>/', MovimentacaoDeleteView.as_view(), name='movimentacao_delete'),
    path('Movimentacao/buscar-produto/', BuscarProdutoPorCodigoView.as_view(), name='buscar_produto_por_codigo'),
]