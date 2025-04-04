from django.contrib import admin
from .models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'num_serie',)
    search_fields = ('nome',)


admin.site.register(Produto, ProdutoAdmin)