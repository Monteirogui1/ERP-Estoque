from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Produto
from .forms import ProdutoForm
from ..categorias.models import Categoria
from ..fornecedor.models import Fornecedor
from ..marcas.models import Marca
from ..movimentacao.models import Movimentacao


class ProdutoListView(ListView):
    model = Produto
    template_name = 'produtos/produtos_list.html'
    context_object_name = 'produto'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        codigo_barras = self.request.GET.get('codigo_barras')
        status = self.request.GET.get('status')
        num_serie = self.request.GET.get('num_serie')
        categoria = self.request.GET.get('categoria')
        marca = self.request.GET.get('marca')
        fornecedor = self.request.GET.get('fornecedor')
        ordernar = self.request.GET.get('ordenar')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        if codigo_barras:
            queryset = queryset.filter(codigo_barras__icontains=codigo_barras)
        if num_serie:
            queryset = queryset.filter(num_serie__icontains=num_serie)
        if fornecedor:
            queryset = queryset.filter(fornecedor__id=fornecedor)
        if marca:
            queryset = queryset.filter(marca__id=marca)
        if status == 'true':
            queryset = queryset.filter(status=True)
        if status == 'false':
            queryset = queryset.filter(status=False)
        if ordernar:
            queryset = queryset.order_by(ordernar)
        else:
            queryset = queryset.order_by('nome')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fornecedores'] = Fornecedor.objects.all()
        context['marcas'] = Marca.objects.all()
        return context



class ProdutoCreateView(CreateView):
    model = Produto
    template_name = 'produtos/produtos_edit.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('produtos:produtos_list')


class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'produtos/produtos_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['movimentacao'] = Movimentacao.objects.filter(produto=self.object).order_by('-created_at')
        return context


class ProdutoUpdateView(UpdateView):
    model = Produto
    template_name = 'produtos/produtos_edit.html'
    form_class = ProdutoForm
    success_url = reverse_lazy('produtos:produtos_list')


class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = 'produtos/deleta_produto.html'
    success_url = reverse_lazy('produtos:produtos_list')

