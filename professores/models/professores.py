import re

from django.core.exceptions import ValidationError
from django.db import models

from autenticacao.models.user import Usuario
from professores.models.universidades import Universidade


def validar_cpf(value):
    digits = re.sub(r'\D', '', value)
    if len(digits) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.')
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
        raise ValidationError('CPF deve estar no formato XXX.XXX.XXX-XX.')


class Professor(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='professores',
    )
    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.PROTECT,
        related_name='professores',
    )
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf])
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, blank=True, default='')
    lattes = models.URLField(blank=True, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'professores'
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return f'{self.usuario} — {self.universidade}'
