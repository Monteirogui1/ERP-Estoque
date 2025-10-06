from django import forms
from django import template
from django.core.exceptions import ValidationError

from .models import Produto, VariacaoProduto

STATUS_CHOICE = ((True, 'Ativo'), (False, 'Inativo'),)

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ['nome', 'status', 'categoria', 'marca', 'fornecedor',
                  'descricao', 'num_serie', 'preco_custo', 'preco_venda', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=STATUS_CHOICE),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'num_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={'class': 'form-control','accept': 'image/*'}),
        }
        labels = {
            'nome': 'Nome',
            'status': 'Status',
            'categoria': 'Categoria',
            'marca': 'Marca',
            'fornecedor': 'Fornecedor',
            'descricao': 'Descrição',
            'num_serie': 'Número de Série',
            'preco_custo': 'Preço de Custo',
            'preco_venda': 'Preço de Venda',
            'imagem': 'Imagem do Produto',
        }

class VariacaoProdutoForm(forms.ModelForm):
    class Meta:
        model = VariacaoProduto
        fields = ['tamanho', 'estoque_minimo', 'codigo_barras', 'unidade']
        widgets = {
            'unidade': forms.Select(attrs={'class': 'form-control'}),
            'tamanho': forms.TextInput(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'tamanho': 'Tamanho',
            'estoque_minimo': 'Estoque Mínimo',
            'codigo_barras': 'Código de Barras'
        }

    def clean_codigo_barras(self):
        """Valida o campo codigo_barras para garantir que seja único e não esteja vazio se preenchido."""
        codigo = self.cleaned_data.get('codigo_barras')
        if codigo and not codigo.strip():
            raise forms.ValidationError("O código de barras não pode conter apenas espaços.")
        return codigo

VariacaoProdutoFormSet = forms.inlineformset_factory(
    Produto, VariacaoProduto, form=VariacaoProdutoForm, extra=1, can_delete=True
)