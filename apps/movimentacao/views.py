from datetime import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from .models import Movimentacao
from .forms import MovimentacaoForm
from ..produtos.models import Produto


class MovimentacaoListView(ListView):
    model =  Movimentacao
    template_name = 'movimentacao/movimentacao_list.html'
    context_object_name = 'movimentacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        produto = self.request.GET.get('produto')
        tipo = self.request.GET.get('tipo')
        quantidade = self.request.GET.get('quantidade')
        data = self.request.GET.get('data')

        if produto:
            queryset = queryset.filter(produto__nome__icontains=produto)
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
        context['produtos'] = Produto.objects.all()
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