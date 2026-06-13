from django.db import models

from estudantes.models.estudantes import Estudante
from turmas.models.turmas import Turma


class EstudanteTurma(models.Model):
    class Status(models.TextChoices):
        PRE_APROVADO = 'pre_aprovado', 'Pré Aprovado'
        ACEITO = 'aceito', 'Aceito'
        RECUSADO = 'recusado', 'Recusado'

    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name='turmas_inscricoes',
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='inscricoes',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRE_APROVADO)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'estudantes_turmas'
        verbose_name = 'Inscrição em Turma'
        verbose_name_plural = 'Inscrições em Turmas'
        unique_together = ('estudante', 'turma')

    def __str__(self):
        return f'{self.estudante} — {self.turma} ({self.status})'
