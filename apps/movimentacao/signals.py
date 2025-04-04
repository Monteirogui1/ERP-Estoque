from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movimentacao
from ..notificacao.models import Notificacao


@receiver(post_save, sender=Movimentacao)
def update_produto_quantidade(sender, instance, created, **kwargs):
    if created and instance.quantidade > 0:
        produto = instance.produto
        if instance.tipo == 'Entrada':
            produto.quantidade += instance.quantidade
        elif instance.tipo == 'Saída':
            produto.quantidade -= instance.quantidade
        produto.save()

        # Verifica se o estoque está abaixo do limite
        if produto.quantidade <= produto.estoque_minimo:
            mensagem = f"O produto {produto.nome} está com estoque baixo: {produto.quantidade} unidades (limite: {produto.estoque_minimo})."
            Notificacao.objects.create(produto=produto, mensagem=mensagem)