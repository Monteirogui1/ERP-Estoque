from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from import_export.signals import post_import
from apps.produtos.models import VariacaoProduto
from .models import Movimentacao, Lote, HistoricoEstoque
from ..notificacao.models import Notificacao
from apps.produtos.resources import VariacaoProdutoResource
from decimal import Decimal
from ..notificacao.utils import enviar_email_estoque_minimo

# Fatores para converter para a "unidade base" do estoque (kg ou L ou UN)
FATORES = {
    'UN': Decimal('1'),      # unidade → unidade
    'ML': Decimal('0.001'),  # ml → L
    'L':  Decimal('1'),      # L → L
    'KG': Decimal('1'),      # kg → kg
    'GR': Decimal('0.001'),  # g → kg
}


@receiver(post_save, sender=Movimentacao)
def update_variacao_quantidade(sender, instance, created, **kwargs):
    if not created or instance.quantidade == 0:
        return

    variacao = instance.produto  # VariacaoProduto
    unidade = variacao.unidade
    fator = FATORES.get(unidade, Decimal('1'))
    q_base = (instance.quantidade * fator).quantize(Decimal('0.01'))

    with transaction.atomic():
        antes = variacao.quantidade

        if instance.tipo == 'Entrada':
            variacao.quantidade += q_base
            motivo = f"Entrada de {instance.quantidade}{unidade}"
        elif instance.tipo == 'Saída':
            if variacao.quantidade < q_base:
                raise ValueError("Estoque insuficiente para esta saída")
            variacao.quantidade -= q_base
            motivo = f"Saída de {instance.quantidade}{unidade}"
        else:
            # caso você venha a adicionar outros tipos no futuro
            motivo = f"{instance.tipo} de {instance.quantidade}{unidade}"
            variacao.quantidade = q_base

        variacao.save()

        # Registrar no histórico
        HistoricoEstoque.objects.create(
            variacao=variacao,
            lote=instance.lote,
            quantidade_anterior=antes,
            quantidade_nova=variacao.quantidade,
            tipo_operacao=instance.tipo,
            motivo=motivo,
            usuario=instance.request.user if hasattr(instance, 'request') else None
        )

        # Notificação de estoque baixo
        if variacao.quantidade <= variacao.estoque_minimo:
            mensagem = (f"O produto {variacao.produto.nome} ({variacao.tamanho}) está com estoque baixo: "
                        f"{variacao.quantidade} unidades (limite: {variacao.estoque_minimo}).")
            Notificacao.objects.create(produto=variacao.produto, mensagem=mensagem)
            enviar_email_estoque_minimo(variacao)

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


@receiver(post_import, sender=VariacaoProdutoResource)
def post_import_variacao(model, **kwargs):
    for instance in VariacaoProduto.objects.all():
        if instance.quantidade <= instance.estoque_minimo:
            mensagem = (f"O produto {instance.produto.nome} ({instance.tamanho}) está com estoque baixo: "
                        f"{instance.quantidade} unidades (limite: {instance.estoque_minimo}).")
            Notificacao.objects.create(produto=instance.produto, mensagem=mensagem)