from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views import View
from .forms import PeriodoForm
from .metrics import metricas_vendas, metricas_estoque
from apps.produtos.models import Produto, VariacaoProduto
from apps.movimentacao.models import Lote, HistoricoEstoque
from apps.notificacao.models import Notificacao


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_inicio = None
        data_fim = timezone.now()

        # Inicializar o formulário com "Hoje" como padrão se não houver parâmetros GET
        initial = {'periodo': 'hoje'} if not self.request.GET else None
        form = PeriodoForm(self.request.GET or initial)

        if form.is_valid():
            periodo = form.cleaned_data['periodo']
            if periodo == 'hoje':
                data_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            elif periodo == 'semana':
                data_inicio = data_fim - timedelta(days=7)
            elif periodo == 'mes':
                data_inicio = data_fim - timedelta(days=30)
            elif periodo == 'ano':
                data_inicio = data_fim - timedelta(days=365)
            elif periodo == 'custom':
                data_inicio = form.cleaned_data['data_inicio']
                data_fim = form.cleaned_data['data_fim']

        context['metricas'] = metricas_vendas(data_inicio, data_fim)
        context['metricas_estoque'] = metricas_estoque()
        context['produtos'] = Produto.objects.all()[:10]
        context['notificacoes'] = Notificacao.objects.filter(lida=False)[:5]
        context['form'] = form
        return context


class SearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if not query:
            return JsonResponse({'results': []})

        produtos = VariacaoProduto.objects.filter(produto__nome__icontains=query).values(
            'id', 'produto__nome', 'tamanho'
        )[:5]
        lotes = Lote.objects.filter(numero_lote__icontains=query).values(
            'id', 'numero_lote', 'variacao__produto__nome'
        )[:5]
        historicos = HistoricoEstoque.objects.filter(variacao__produto__nome__icontains=query).values(
            'id', 'variacao__produto__nome', 'tipo_operacao', 'created_at'
        )[:5]

        results = [
            {
                'type': 'produto',
                'id': p['id'],
                'nome': f"{p['produto__nome']} ({p['tamanho']})",
                'url': f"/produtos/{p['id']}/detalhe/"
            } for p in produtos
        ] + [
            {
                'type': 'lote',
                'id': l['id'],
                'nome': f"Lote {l['numero_lote']} - {l['variacao__produto__nome']}",
                'url': f"/movimentacao/lote/{l['id']}/detalhe/"
            } for l in lotes
        ] + [
            {
                'type': 'historico',
                'id': h['id'],
                'nome': f"Histórico: {h['variacao__produto__nome']} - {h['tipo_operacao']}",
                'url': f"/movimentacao/historico-estoque/{h['id']}/detalhe/"
            } for h in historicos
        ]

        return JsonResponse({'results': results})