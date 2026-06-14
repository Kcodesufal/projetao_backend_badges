import uuid

from django.db import models

from estudantes.models.estudantes import Estudante
from projetos.models.projeto import Projeto


class Certificado(models.Model):
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name='certificados',
    )
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='certificados',
    )
    carga_horaria = models.PositiveIntegerField(help_text='Total de horas cumpridas no projeto')
    codigo_verificacao = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    data_emissao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificados'
        verbose_name = 'Certificado'
        verbose_name_plural = 'Certificados'
        unique_together = ('estudante', 'projeto')
        ordering = ['-data_emissao']

    def __str__(self):
        return f'Certificado — {self.estudante} / {self.projeto} ({self.carga_horaria}h)'
