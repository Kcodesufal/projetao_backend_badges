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


class Estudante(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='estudantes',
    )
    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.PROTECT,
        related_name='estudantes',
    )
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf])
    data_nascimento = models.DateField()
    matricula = models.CharField(max_length=50, unique=True)
    curso = models.CharField(max_length=255)
    periodo_curso = models.PositiveSmallIntegerField(help_text='Período atual do curso (ex: 5)')
    telefone = models.CharField(max_length=20, blank=True, default='')
    lattes = models.URLField(blank=True, default='')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'estudantes'
        verbose_name = 'Estudante'
        verbose_name_plural = 'Estudantes'

    def __str__(self):
        return f'{self.usuario} — {self.matricula}'
