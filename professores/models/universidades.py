from django.db import models


class Universidade(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'universidades'
        verbose_name = 'Universidade'
        verbose_name_plural = 'Universidades'
        ordering = ['nome']

    def __str__(self):
        return self.nome
