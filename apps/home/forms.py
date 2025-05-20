from django import forms
from django.utils import timezone


class PeriodoForm(forms.Form):
    PERIODO_CHOICES = [
        ('hoje', 'Hoje'),
        ('semana', 'Última Semana'),
        ('mes', 'Último Mês'),
        ('ano', 'Último Ano'),
        ('custom', 'Personalizado'),
    ]

    periodo = forms.ChoiceField(
        choices=PERIODO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='hoje',
        label='Período'
    )
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data Início'
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data Fim'
    )

    def clean(self):
        cleaned_data = super().clean()
        periodo = cleaned_data.get('periodo')
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if periodo == 'custom':
            if not data_inicio or not data_fim:
                raise forms.ValidationError("As datas de início e fim são obrigatórias para o período personalizado.")
            if data_inicio > data_fim:
                raise forms.ValidationError("A data de início não pode ser posterior à data de fim.")
            if data_fim > timezone.now().date():
                raise forms.ValidationError("A data de fim não pode ser futura.")

        return cleaned_data