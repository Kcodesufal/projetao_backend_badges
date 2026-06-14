from django.db import models

from atividades.models.atividade import Atividade
from professores.models.professores import Professor
from turmas.models.turmas import Turma
from estudantes.models.estudantes import Estudante


class Aplicacao(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        ACEITA = 'aceita', 'Aceita'
        RECUSADA = 'recusada', 'Recusada'

    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='aplicacoes',
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='aplicacoes',
    )
    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.CASCADE,
        related_name='aplicacoes',
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    justificativa = models.TextField(blank=True, default='', help_text='Motivação do professor para participar')
    feedback_ong = models.TextField(blank=True, default='', help_text='Resposta da ONG ao aceitar ou recusar')
    estudantes_rejeitados = models.ManyToManyField(
        Estudante,
        blank=True,
        related_name='aplicacoes_rejeitadas',
    )
    data_aplicacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'aplicacoes'
        verbose_name = 'Aplicação'
        verbose_name_plural = 'Aplicações'
        unique_together = ('professor', 'turma', 'atividade')
        ordering = ['-data_aplicacao']

    def __str__(self):
        return f'{self.professor} → {self.atividade} ({self.status})'
