from django.db import models

from apps.produtos.models import Produto


class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacao',
                                limit_choices_to={'status': True},)
    tipo = models.CharField(max_length=10)
    quantidade = models.IntegerField()
    descricao = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{str(self.produto)} - {self.tipo} - {self.quantidade}"
