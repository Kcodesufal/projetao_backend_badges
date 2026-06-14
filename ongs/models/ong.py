import re

from django.core.exceptions import ValidationError
from django.db import models

from autenticacao.models.user import Usuario
from ongs.enums.causa_social import CausaSocial


def validar_cnpj(value):
    if not re.match(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', value):
        raise ValidationError('CNPJ deve estar no formato XX.XXX.XXX/XXXX-XX.')


class Ong(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='ongs',
    )
    cnpj = models.CharField(max_length=18, unique=True, validators=[validar_cnpj])
    razao_social = models.CharField(max_length=255)
    causa_social = models.CharField(max_length=50, choices=CausaSocial.choices)
    avaliacao_media = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text='Média das avaliações recebidas (0 a 10)',
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ongs'
        verbose_name = 'ONG'
        verbose_name_plural = 'ONGs'

    def __str__(self):
        return self.razao_social
