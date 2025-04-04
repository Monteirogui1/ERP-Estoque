from lib2to3.fixes.fix_input import context

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .metrics import metricas_produtos, metricas_vendas, metricas_saidas
from django.contrib.auth.decorators import login_required



# PÁGINA PRINCIPAL
# ----------------------------------------------

class IndexTemplateView(TemplateView):
    template_name = "home/home.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produtos_metricas = metricas_produtos()
        vendas_metricas = metricas_vendas()
        saidas = metricas_saidas()

        context['produtos_metricas'] = produtos_metricas
        context['vendas_metricas'] = vendas_metricas
        context['saidas'] = saidas

        return context