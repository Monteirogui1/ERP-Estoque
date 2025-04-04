from django.db import models


class Fornecedor(models.Model):
    nome = models.CharField(max_length=500)
    contato = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    descricao = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome