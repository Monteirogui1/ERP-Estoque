from django import forms

from .models import Movimentacao

TIPO_CHOICES = (('Entrada', 'Entrada'), ('Saída', 'Saída'))

class MovimentacaoForm(forms.ModelForm):

    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tipo'
    )

    class Meta:
        model = Movimentacao
        fields = ['produto', 'tipo', 'quantidade', 'descricao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'produto': 'Produto',
            'tipo': 'Tipo de Operação',
            'quantidade': 'Quantidade',
            'descricao': 'Descrição',
        }
        