from datetime import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, View
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator

from .models import Movimentacao
from .forms import MovimentacaoForm
from ..produtos.models import Produto, VariacaoProduto


class MovimentacaoListView(ListView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_list.html'
    context_object_name = 'movimentacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')  # Alterado de 'variacao' para 'produto' para clareza no frontend
        tipo = self.request.GET.get('tipo')
        quantidade = self.request.GET.get('quantidade')
        data = self.request.GET.get('data')

        if produto:
            queryset = queryset.filter(produto__produto__nome__icontains=produto)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if quantidade:
            try:
                quantidade = int(quantidade)
                queryset = queryset.filter(quantidade=quantidade)
            except ValueError:
                pass
        if data:
            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d')
                queryset = queryset.filter(created_at__date=data_obj)
            except ValueError:
                pass  # Ignora se o formato da data estiver errado

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = MovimentacaoForm().fields['tipo'].choices
        context['produtos'] = Produto.objects.all()  # Mantido para o filtro, mas considere listar variações se necessário
        return context


class MovimentacaoCreateView(CreateView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_create.html'
    form_class = MovimentacaoForm
    success_url = reverse_lazy('movimentacao:movimentacao_list')


class MovimentacaoDetailView(DetailView):
    model = Movimentacao
    template_name = 'movimentacao/detalhe_entrada.html'


class MovimentacaoDeleteView(DeleteView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_delete.html'
    success_url = reverse_lazy('movimentacao:movimentacao_list')


class BuscarProdutoPorCodigoView(View):
    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        codigo = request.GET.get('codigo_barras', '')
        if not codigo:
            return JsonResponse({'error': 'Código de barras não fornecido'}, status=400)

        try:
            variacao = VariacaoProduto.objects.get(codigo_barras=codigo)
            return JsonResponse({
                'id': variacao.id,
                'nome': f"{variacao.produto.nome} - {variacao.tamanho}",
                'quantidade': variacao.quantidade,
            })
        except VariacaoProduto.DoesNotExist:
            return JsonResponse({'error': 'Variação de produto não encontrada'}, status=404)