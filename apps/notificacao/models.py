from django.db import models

from apps.produtos.models import Produto


class Notificacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='produtos')
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.produto.nome} - {self.created_at}"