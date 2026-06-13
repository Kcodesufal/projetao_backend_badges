from django.db import models

from professores.models.professores import Professor
from turmas.models.turmas import Turma


class TurmaProfessor(models.Model):
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        related_name='turmas_professor',
    )
    turma = models.ForeignKey(
        Turma,
        on_delete=models.CASCADE,
        related_name='turmas_professor',
    )
    data_vinculo = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'turmas_professor'
        verbose_name = 'Turma do Professor'
        verbose_name_plural = 'Turmas dos Professores'
        unique_together = ('professor', 'turma')

    def __str__(self):
        return f'{self.professor} — {self.turma}'
