from django.db.models import Sum, F
from django.utils.formats import number_format

from ..movimentacao.models import Movimentacao
from ..produtos.models import Produto, VariacaoProduto

def metricas_produtos():
    total_preco_custo = VariacaoProduto.objects.aggregate(
        total=Sum(F('produto__preco_custo') * F('quantidade')))['total'] or 0
    total_preco_venda = VariacaoProduto.objects.aggregate(
        total=Sum(F('produto__preco_venda') * F('quantidade')))['total'] or 0
    total_quantidade = VariacaoProduto.objects.aggregate(
        total=Sum('quantidade') )['total'] or 0
    total_lucro = total_preco_venda - total_preco_custo

    return dict(
        total_preco_custo=number_format(total_preco_custo, decimal_pos=2, force_grouping=True),
        total_preco_venda=number_format(total_preco_venda, decimal_pos=2, force_grouping=True),
        total_quantidade=total_quantidade,
        total_lucro=number_format(total_lucro, decimal_pos=2, force_grouping=True),
    )


def metricas_vendas():
    vendas = Movimentacao.objects.filter(tipo='Saída')

    total_vendas = vendas.count()

    total_produtos_vendidos = vendas.aggregate(
        total_produtos_vendidos=Sum('quantidade'))['total_produtos_vendidos'] or 0
    total_valor_vendas = vendas.aggregate(
        total_valor_vendas=Sum('quantidade') * F('produto__produto__preco_venda'))['total_valor_vendas'] or 0
    total_valor_custo = vendas.aggregate(
        total_valor_custo=Sum('quantidade') * F('produto__produto__preco_custo'))['total_valor_custo'] or 0
    total_valor_lucro = total_valor_vendas - total_valor_custo

    return dict(
        total_vendas=total_vendas,
        total_produtos_vendidos=total_produtos_vendidos,
        total_valor_vendas=number_format(total_valor_vendas, decimal_pos=2, force_grouping=True),
        total_valor_lucro=number_format(total_valor_lucro, decimal_pos=2, force_grouping=True),
    )


def metricas_saidas():
    vendas = VariacaoProduto.objects.filter(movimentacao__tipo="Saída")

    top_produtos = vendas.annotate(total_vendido=Sum('movimentacao__quantidade')).order_by('-total_vendido')[:10]
    bad_produtos = vendas.annotate(sem_saidas=Sum('movimentacao__quantidade')).order_by('sem_saidas')[:10]

    return dict(
        total_vendas=top_produtos,
        sem_saidas=bad_produtos,
    )

