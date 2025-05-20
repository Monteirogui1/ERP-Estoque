from django import forms

class ImportForm(forms.Form):
    file_format = forms.ChoiceField(
        choices=(
            ('CSV', 'CSV'),
            ('JSON', 'JSON'),
            ('XLSX', 'XLSX'),
        ),
        label='Formato do Arquivo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    import_file = forms.FileField(
        label='Arquivo para Importação',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )