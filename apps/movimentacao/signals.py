from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import Movimentacao, Lote, HistoricoEstoque
from ..notificacao.models import Notificacao


@receiver(post_save, sender=Movimentacao)
def update_produto_quantidade(sender, instance, created, **kwargs):
    if created and instance.quantidade != 0:
        with transaction.atomic():
            produto = instance.produto
            quantidade_anterior = produto.quantidade
            if instance.tipo == 'Entrada':
                produto.quantidade += instance.quantidade
                motivo = f"Entrada de {instance.quantidade} unidades via movimentação."
            elif instance.tipo == 'Saída':
                if produto.quantidade < instance.quantidade:
                    raise ValueError("Estoque insuficiente para esta saída")
                produto.quantidade -= instance.quantidade
                motivo = f"Saída de {instance.quantidade} unidades via movimentação."
            elif instance.tipo == 'Ajuste':
                if instance.quantidade < 0:
                    raise ValueError("Quantidade de ajuste não pode ser negativa")
                produto.quantidade = instance.quantidade
                motivo = f"Ajuste manual para {instance.quantidade} unidades."
            produto.save()

            # Registrar no histórico
            HistoricoEstoque.objects.create(
                variacao=produto,
                lote=instance.lote,
                quantidade_anterior=quantidade_anterior,
                quantidade_nova=produto.quantidade,
                tipo_operacao=instance.tipo,
                motivo=motivo,
                usuario=instance.request.user if hasattr(instance, 'request') else None
            )

            if produto.quantidade <= produto.estoque_minimo:
                mensagem = (f"O produto {produto.produto.nome} ({produto.tamanho}) está com estoque baixo: "
                            f"{produto.quantidade} unidades (limite: {produto.estoque_minimo}).")
                Notificacao.objects.create(produto=produto.produto, mensagem=mensagem)


@receiver(post_save, sender=Lote)
def update_variacao_quantidade(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            variacao = instance.variacao
            quantidade_anterior = variacao.quantidade
            variacao.quantidade += instance.quantidade
            variacao.save()

            # Registrar no histórico
            HistoricoEstoque.objects.create(
                variacao=variacao,
                lote=instance,
                quantidade_anterior=quantidade_anterior,
                quantidade_nova=variacao.quantidade,
                tipo_operacao='Lote Criado',
                motivo=f"Criação de lote {instance.numero_lote} com {instance.quantidade} unidades.",
                usuario=instance.request.user if hasattr(instance, 'request') else None
            )

            if variacao.quantidade <= variacao.estoque_minimo:
                mensagem = (f"O produto {variacao.produto.nome} ({variacao.tamanho}) está com estoque baixo: "
                            f"{variacao.quantidade} unidades (limite: {variacao.estoque_minimo}).")
                Notificacao.objects.create(produto=variacao.produto, mensagem=mensagem)


@receiver(post_delete, sender=Lote)
def revert_variacao_quantidade(sender, instance, **kwargs):
    with transaction.atomic():
        variacao = instance.variacao
        quantidade_anterior = variacao.quantidade
        variacao.quantidade -= instance.quantidade
        if variacao.quantidade < 0:
            raise ValueError("Estoque não pode ser negativo após exclusão do lote.")
        variacao.save()

        # Registrar no histórico
        HistoricoEstoque.objects.create(
            variacao=variacao,
            lote=instance,
            quantidade_anterior=quantidade_anterior,
            quantidade_nova=variacao.quantidade,
            tipo_operacao='Lote Excluído',
            motivo=f"Exclusão de lote {instance.numero_lote} com {instance.quantidade} unidades.",
            usuario=None
        )