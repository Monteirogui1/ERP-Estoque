from django.db.models import Sum, F, FloatField
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from apps.movimentacao.models import Movimentacao
from apps.produtos.models import Produto, VariacaoProduto
from datetime import datetime, timedelta
from django.utils import timezone


def metricas_vendas(data_inicio=None, data_fim=None):
    vendas = Movimentacao.objects.filter(tipo__nome='Saida')
    entradas = Movimentacao.objects.filter(tipo__nome='Entrada')

    if data_inicio and data_fim:
        vendas = vendas.filter(data__range=[data_inicio, data_fim])
        entradas = entradas.filter(data__range=[data_inicio, data_fim])

    # Somar corretamente o valor total das vendas e custo (compatível com SQLite)
    vendas = vendas.annotate(
        subtotal_venda=F('quantidade') * F('variacao__produto__preco_venda'),
        subtotal_custo=F('quantidade') * F('variacao__produto__preco_custo'),
    )
    total_vendas = vendas.count()
    total_produtos_vendidos = vendas.aggregate(total=Sum('quantidade'))['total'] or 0
    total_valor_vendas = vendas.aggregate(total=Sum('subtotal_venda', output_field=FloatField()))['total'] or 0
    total_valor_custo = vendas.aggregate(total=Sum('subtotal_custo', output_field=FloatField()))['total'] or 0
    total_lucro = total_valor_vendas - total_valor_custo

    entradas = entradas.annotate(
        subtotal_entrada=F('quantidade') * F('variacao__produto__preco_custo')
    )
    total_entradas = entradas.count()
    total_produtos_entradas = entradas.aggregate(total=Sum('quantidade'))['total'] or 0
    total_valor_entradas = entradas.aggregate(total=Sum('subtotal_entrada', output_field=FloatField()))['total'] or 0

    produtos_mais_vendidos = vendas.values(
        'variacao__produto__nome', 'variacao__tamanho'
    ).annotate(
        total_vendido=Sum('quantidade')
    ).order_by('-total_vendido')[:10]

    produtos_menos_vendidos = vendas.values(
        'variacao__produto__nome', 'variacao__tamanho'
    ).annotate(
        total_vendido=Sum('quantidade')
    ).order_by('total_vendido')[:10]

    vendas_por_categoria = vendas.values(
        'variacao__produto__categoria__nome'
    ).annotate(
        total_vendido=Sum('quantidade'),
        valor_total=Sum('subtotal_venda', output_field=FloatField())
    ).order_by('-total_vendido')

    # Calcular vendas por período (temporal)
    if data_inicio and data_fim:
        delta = data_fim - data_inicio
        if delta.days <= 7:  # Período curto: agrupar por dia
            trunc = TruncDay
            date_format = '%d/%m/%Y'
        elif delta.days <= 30:  # Período médio: agrupar por semana
            trunc = TruncWeek
            date_format = 'Semana %U/%Y'
        else:  # Período longo: agrupar por mês
            trunc = TruncMonth
            date_format = '%b/%Y'

        vendas_por_periodo_qs = vendas.annotate(
            periodo=trunc('data')
        ).values(
            'periodo'
        ).annotate(
            valor_total=Sum('subtotal_venda', output_field=FloatField())
        ).order_by('periodo')

        # Formatar labels e valores
        vendas_por_periodo = [
            {
                'label': item['periodo'].strftime(date_format) if item['periodo'] else 'Sem data',
                'valor_total': float(item['valor_total']) if item['valor_total'] else 0
            } for item in vendas_por_periodo_qs
        ]
    else:
        vendas_por_periodo = []

    return {
        'total_vendas': total_vendas,
        'total_produtos_vendidos': total_produtos_vendidos,
        'total_valor_vendas': total_valor_vendas,
        'total_valor_custo': total_valor_custo,
        'total_lucro': total_lucro,
        'total_entradas': total_entradas,
        'total_produtos_entradas': total_produtos_entradas,
        'total_valor_entradas': total_valor_entradas,
        'produtos_mais_vendidos': list(produtos_mais_vendidos),
        'produtos_menos_vendidos': list(produtos_menos_vendidos),
        'vendas_por_categoria': list(vendas_por_categoria),
        'vendas_por_periodo': vendas_por_periodo,
    }


def metricas_estoque():
    produtos = VariacaoProduto.objects.all()
    produtos = produtos.annotate(
        subtotal_custo=F('quantidade') * F('produto__preco_custo'),
        subtotal_venda=F('quantidade') * F('produto__preco_venda'),
    )
    total_estoque = produtos.aggregate(total=Sum('quantidade'))['total'] or 0
    total_valor_custo = produtos.aggregate(total=Sum('subtotal_custo', output_field=FloatField()))['total'] or 0
    total_valor_venda = produtos.aggregate(total=Sum('subtotal_venda', output_field=FloatField()))['total'] or 0
    total_lucro_estimado = total_valor_venda - total_valor_custo

    return {
        'total_estoque': total_estoque,
        'total_valor_custo': total_valor_custo,
        'total_valor_venda': total_valor_venda,
        'total_lucro_estimado': total_lucro_estimado,
    }
