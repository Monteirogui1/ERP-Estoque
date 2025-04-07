from django import forms
from .models import Produto


STATUS_CHOICE = ((True, 'Ativo'), (False, 'Inativo'),)

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        fields = ['nome', 'status', 'codigo_barras', 'categoria', 'marca', 'fornecedor', 'estoque_minimo',
                  'descricao', 'num_serie', 'preco_custo', 'preco_venda', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escaneie ou digite o código de barras'}),
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
            'codigo_barras': 'Código de Barras',
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

    def clean_codigo_barras(self):
        """Valida o campo codigo_barras para garantir que não esteja vazio se preenchido."""
        codigo = self.cleaned_data.get('codigo_barras')
        if codigo and not codigo.strip():
            raise forms.ValidationError("O código de barras não pode conter apenas espaços.")
        return codigo