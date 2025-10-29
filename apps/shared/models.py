from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    dominio = models.CharField(max_length=100, unique=True, help_text="subdomínio ou nome identificador (ex: loja1)")
    banco = models.CharField(max_length=100, unique=True, help_text="nome do banco em settings.py")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome