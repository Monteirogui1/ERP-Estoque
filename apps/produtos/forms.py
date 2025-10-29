from django import forms
from .models import Produto, VariacaoProduto, UnidadeMedida, CampoDinamico

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'categoria', 'marca', 'fornecedor', 'descricao', 'num_serie',
            'preco_custo', 'preco_venda', 'imagem', 'status'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'num_serie': 'Nº Série',
            'preco_custo': 'Preço de Custo',
            'preco_venda': 'Preço de Venda',
            'imagem': 'Imagem do Produto',
            'status': 'Ativo'
        }
        help_texts = {
            'status': 'Desmarque para ocultar este produto nas vendas.',
            'imagem': 'Imagem principal do produto.',
        }

class VariacaoProdutoForm(forms.ModelForm):
    class Meta:
        model = VariacaoProduto
        fields = [
            'tamanho', 'quantidade', 'unidade', 'estoque_minimo',
            'codigo_barras', 'barcode_image', 'qr_code'
        ]
        labels = {
            'tamanho': 'Tamanho/Cor/Var.',
            'quantidade': 'Qtd. Estoque',
            'unidade': 'Unidade de Medida',
            'estoque_minimo': 'Estoque Mínimo',
            'codigo_barras': 'Código de Barras',
            'barcode_image': 'Imagem Código de Barras',
            'qr_code': 'QR Code',
        }
        widgets = {
            'quantidade': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'tamanho': 'Exemplo: P, M, G, 500ml, Azul.',
        }

from django.forms import inlineformset_factory

VariacaoProdutoFormSet = inlineformset_factory(
    Produto, VariacaoProduto,
    form=VariacaoProdutoForm,
    extra=1, can_delete=True, min_num=0, validate_min=True
)

class UnidadeMedidaForm(forms.ModelForm):
    class Meta:
        model = UnidadeMedida
        fields = ['nome', 'sigla']
        labels = {
            'nome': 'Nome da Unidade',
            'sigla': 'Sigla (ex: UN, KG, L)',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 10}),
        }

class CampoDinamicoForm(forms.ModelForm):
    class Meta:
        model = CampoDinamico
        fields = ['nome', 'categoria', 'tipo', 'obrigatorio']
        labels = {
            'nome': 'Nome do Campo',
            'categoria': 'Categoria',
            'tipo': 'Tipo do Campo',
            'obrigatorio': 'Obrigatório?',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'obrigatorio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
