from django.db import models

from apps.categorias.models import Categoria
from apps.fornecedor.models import Fornecedor
from apps.marcas.models import Marca


class UnidadeMedida(models.TextChoices):
    UNIDADE = 'UN', 'Unidade'
    MILILITRO = 'ML', 'Mililitro'
    LITRO = 'L', 'Litro'
    QUILOGRAMA = 'KG', 'Quilograma'
    GRAMA = 'G', 'Grama'


class Produto(models.Model):
    nome = models.CharField(max_length=500)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos',
                                  limit_choices_to={'status': True},)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='produtos',
                              limit_choices_to={'status': True},)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='produtos',
                                   limit_choices_to={'status': True},)
    descricao = models.TextField(null=True, blank=True)
    num_serie = models.CharField(max_length=200, null=True, blank=True)
    preco_custo = models.DecimalField(max_digits=20, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=20, decimal_places=2)
    imagem = models.ImageField(null=True, blank=True, upload_to='produtos/')
    status = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class VariacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    tamanho = models.CharField(max_length=10)
    quantidade = models.PositiveIntegerField(default=0)
    unidade = models.CharField(max_length=2, choices=UnidadeMedida.choices, default=UnidadeMedida.UNIDADE,
                               help_text="Selecione a unidade de medida"
                               )
    estoque_minimo = models.PositiveIntegerField(default=10)
    codigo_barras = models.CharField(max_length=128, null=True, blank=True)
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    class Meta:
        ordering = ['tamanho']

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho}"
