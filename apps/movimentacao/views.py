from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils.decorators import method_decorator
from django.views import View
from .models import Movimentacao, Lote, HistoricoEstoque
from .forms import MovimentacaoForm, LoteForm, HistoricoEstoqueForm
from ..produtos.models import Produto, VariacaoProduto
from ..fornecedor.models import Fornecedor
from django.contrib.auth.models import User


class LoteListView(LoginRequiredMixin, ListView):
    model = Lote
    template_name = 'movimentacao/lote_list.html'
    context_object_name = 'lotes'

    def get_queryset(self):
        queryset = super().get_queryset()
        numero_lote = self.request.GET.get('numero_lote')
        produto = self.request.GET.get('produto')
        fornecedor = self.request.GET.get('fornecedor')
        data = self.request.GET.get('data')

        if numero_lote:
            queryset = queryset.filter(numero_lote__icontains=numero_lote)
        if produto:
            queryset = queryset.filter(variacao__produto__nome__icontains=produto)
        if fornecedor:
            queryset = queryset.filter(fornecedor__nome__icontains=fornecedor)
        if data:
            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d')
                queryset = queryset.filter(data_entrada__date=data_obj)
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        context['fornecedores'] = Fornecedor.objects.all()
        return context


class LoteCreateView(LoginRequiredMixin, CreateView):
    model = Lote
    template_name = 'movimentacao/lote_create.html'
    form_class = LoteForm
    success_url = reverse_lazy('movimentacao:lote_list')


class LoteDetailView(LoginRequiredMixin, DetailView):
    model = Lote
    template_name = 'movimentacao/lote_detail.html'
    context_object_name = 'lote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimentacoes'] = Movimentacao.objects.filter(lote=self.object).order_by('-created_at')
        return context


class LoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Lote
    template_name = 'movimentacao/lote_create.html'
    form_class = LoteForm
    success_url = reverse_lazy('movimentacao:lote_list')


class LoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Lote
    template_name = 'movimentacao/lote_delete.html'
    success_url = reverse_lazy('movimentacao:lote_list')


class MovimentacaoListView(LoginRequiredMixin, ListView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_list.html'
    context_object_name = 'movimentacao'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')
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
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = MovimentacaoForm().fields['tipo'].choices
        context['produtos'] = Produto.objects.all()
        return context


class MovimentacaoCreateView(LoginRequiredMixin, CreateView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_create.html'
    form_class = MovimentacaoForm
    success_url = reverse_lazy('movimentacao:movimentacao_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['request'] = self.request
        return kwargs


class MovimentacaoDetailView(LoginRequiredMixin, DetailView):
    model = Movimentacao
    template_name = 'movimentacao/detalhe_entrada.html'


class MovimentacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Movimentacao
    template_name = 'movimentacao/movimentacao_delete.html'
    success_url = reverse_lazy('movimentacao:movimentacao_list')


class HistoricoEstoqueListView(LoginRequiredMixin, ListView):
    model = HistoricoEstoque
    template_name = 'movimentacao/historico_estoque_list.html'
    context_object_name = 'historicos'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')
        tipo = self.request.GET.get('tipo_operacao')
        usuario = self.request.GET.get('usuario')
        data = self.request.GET.get('data')

        if produto:
            queryset = queryset.filter(variacao__produto__nome__icontains=produto)
        if tipo:
            queryset = queryset.filter(tipo_operacao=tipo)
        if usuario:
            queryset = queryset.filter(usuario__username__icontains=usuario)
        if data:
            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d')
                queryset = queryset.filter(created_at__date=data_obj)
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all()
        context['tipos'] = HistoricoEstoque.TIPO_OPERACAO
        context['usuarios'] = User.objects.all()
        return context


class HistoricoEstoqueDetailView(LoginRequiredMixin, DetailView):
    model = HistoricoEstoque
    template_name = 'movimentacao/historico_estoque_detail.html'
    context_object_name = 'historico'


class AjusteEstoqueCreateView(LoginRequiredMixin, CreateView):
    model = Movimentacao
    template_name = 'movimentacao/ajuste_estoque_create.html'
    form_class = HistoricoEstoqueForm
    success_url = reverse_lazy('movimentacao:historico_estoque_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['request'] = self.request
        return kwargs


class BuscarProdutoPorCodigoView(LoginRequiredMixin, View):
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


class ValidarNumeroLoteView(LoginRequiredMixin, View):
    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        numero_lote = request.GET.get('numero_lote', '')
        exists = Lote.objects.filter(numero_lote=numero_lote).exists()
        return JsonResponse({'exists': exists})