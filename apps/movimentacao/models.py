from django.db import models
from django.contrib.auth.models import User
from apps.produtos.models import Produto, VariacaoProduto
from apps.fornecedor.models import Fornecedor


class Lote(models.Model):
    variacao = models.ForeignKey(VariacaoProduto, on_delete=models.PROTECT, related_name='lotes')
    numero_lote = models.CharField(max_length=100, unique=True)
    data_entrada = models.DateTimeField(auto_now_add=True)
    quantidade = models.PositiveIntegerField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='lotes')
    descricao = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'

    def __str__(self):
        return f"Lote {self.numero_lote} - {self.variacao}"


class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('Entrada', 'Entrada'),
        ('Saída', 'Saída'),
    )

    produto = models.ForeignKey(VariacaoProduto, on_delete=models.PROTECT, related_name='movimentacao')
    lote = models.ForeignKey(Lote, on_delete=models.PROTECT, related_name='movimentacoes', null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    descricao = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.produto.produto.nome} - {self.tipo} - {self.quantidade}"


class HistoricoEstoque(models.Model):
    TIPO_OPERACAO = (
        ('Entrada', 'Entrada'),
        ('Saída', 'Saída'),
        ('Ajuste', 'Ajuste'),
        ('Lote Criado', 'Lote Criado'),
        ('Lote Excluído', 'Lote Excluído'),
    )

    variacao = models.ForeignKey(VariacaoProduto, on_delete=models.PROTECT, related_name='historico')
    lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, related_name='historico', null=True, blank=True)
    quantidade_anterior = models.PositiveIntegerField()
    quantidade_nova = models.PositiveIntegerField()
    tipo_operacao = models.CharField(max_length=20, choices=TIPO_OPERACAO)
    motivo = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Histórico de Estoque'
        verbose_name_plural = 'Históricos de Estoque'

    def __str__(self):
        return f"{self.variacao.produto.nome} - {self.tipo_operacao} - {self.created_at|date:'d/m/Y H:i'}"