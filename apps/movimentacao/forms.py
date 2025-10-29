from django import forms
from .models import Lote, Movimentacao, HistoricoEstoque, TipoMovimentacao


class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['variacao', 'numero_lote', 'quantidade', 'fornecedor', 'descricao']
        widgets = {
            'variacao': forms.Select(attrs={'class': 'form-control', 'autofocus': True}),
            'numero_lote': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: LOTE2025-001'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecione o fornecedor'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição opcional do lote'}),
        }
        labels = {
            'variacao': 'Variação do Produto',
            'numero_lote': 'Número do Lote',
            'quantidade': 'Quantidade',
            'fornecedor': 'Fornecedor',
            'descricao': 'Descrição',
        }

    def clean_numero_lote(self):
        numero_lote = self.cleaned_data.get('numero_lote')
        if not numero_lote.strip():
            raise forms.ValidationError("O número do lote não pode estar vazio.")
        if Lote.objects.filter(numero_lote=numero_lote).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este número de lote já está em uso.")
        return numero_lote

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantidade


class MovimentacaoForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=Movimentacao.TIPO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'autofocus': True}),
        label='Tipo'
    )

    class Meta:
        model = Movimentacao
        fields = ['produto', 'lote', 'tipo', 'quantidade', 'descricao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecione o produto'}),
            'lote': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecione o lote (opcional)'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 50'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição da movimentação'}),
        }
        labels = {
            'produto': 'Produto',
            'lote': 'Lote',
            'tipo': 'Tipo de Operação',
            'quantidade': 'Quantidade',
            'descricao': 'Descrição',
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        tipo = self.cleaned_data.get('tipo')
        if tipo != 'Ajuste' and quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero para Entrada ou Saída.")
        return quantidade


class HistoricoEstoqueForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'descricao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control', 'autofocus': True}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: 100'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motivo do ajuste'}),
        }
        labels = {
            'produto': 'Variação do Produto',
            'quantidade': 'Nova Quantidade',
            'descricao': 'Motivo do Ajuste',
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade < 0:
            raise forms.ValidationError("A quantidade não pode ser negativa.")
        return quantidade

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.tipo = 'Ajuste'
        instance.request = self.initial.get('request')  # Passar request para o signal
        if commit:
            instance.save()
        return instance


class TipoMovimentacaoForm(forms.ModelForm):
    class Meta:
        model = TipoMovimentacao
        fields = ['nome', 'entrada_saida', 'descricao']
        labels = {
            'nome': 'Nome do Tipo',
            'entrada_saida': 'Entrada ou Saída?',
            'descricao': 'Descrição',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }