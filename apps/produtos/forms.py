from django import forms
from .models import Produto


STATUS_CHOICE = ((True, 'Ativo'), (False, 'Inativo'),)

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ['nome', 'status', 'categoria', 'marca', 'fornecedor', 'estoque_minimo',
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
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
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
            'estoque_minimo': 'Estoque Minimo',
            'imagem': 'Imagem do Produto',
        }