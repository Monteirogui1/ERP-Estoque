from django.db import models

from apps.categorias.models import Categoria
from apps.fornecedor.models import Fornecedor
from apps.marcas.models import Marca


class Produto(models.Model):
    nome = models.CharField(max_length=500)
    codigo_barras = models.CharField(max_length=128, unique=True, null=True, blank=True)
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
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=10)
    imagem = models.ImageField(null=True, blank=True, upload_to='produtos/')
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome