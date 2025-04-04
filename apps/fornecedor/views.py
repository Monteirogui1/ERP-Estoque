from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .forms import FornecedorForm
from .models import Fornecedor
from ..produtos.models import Produto

app_name = 'fornecedores'


class FornecedorListView(ListView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedores_list.html'
    context_object_name = 'fornecedores'

    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        status = self.request.GET.get('status')
        contato = self.request.GET.get('contato')
        email = self.request.GET.get('email')
        descricao = self.request.GET.get('descricao')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        if descricao:
            queryset = queryset.filter(nome__icontains=descricao)
        if contato:
            queryset = queryset.filter(contato__icontains=contato)
        if email:
            queryset = queryset.filter(email__icontains=email)
        if status == 'true':
            queryset = queryset.filter(status=True)
        if status == 'false':
            queryset = queryset.filter(status=False)

        return queryset


class FornecedorCreateView(CreateView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedores_edit.html'
    form_class = FornecedorForm
    success_url = reverse_lazy('fornecedores:fornecedores_list')


class FornecedorDetailView(DetailView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedores_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['produtos'] = Produto.objects.filter(fornecedor=self.object).order_by('-created_at')
        return context


class FornecedorUpdateView(UpdateView):
    model = Fornecedor
    template_name = 'fornecedor/fornecedores_edit.html'
    form_class = FornecedorForm
    success_url = reverse_lazy('fornecedores:fornecedores_list')


class FornecedorDeleteView(DeleteView):
    model = Fornecedor
    template_name = 'fornecedor/deleta_fornecedor.html'
    success_url = reverse_lazy('fornecedores:fornecedores_list')