from django.contrib import admin
from .models import Cliente
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dominio', 'banco', 'criado_em')
    change_list_template = 'shared/cliente_changelist.html'
