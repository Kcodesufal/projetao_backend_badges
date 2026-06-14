from django.db import models

from estudantes.models.estudantes import Estudante
from projetos.models.projeto import Projeto


class HistoricoEstudante(models.Model):
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name='historico',
    )
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='historico',
    )
    pontos = models.PositiveIntegerField()
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historico_estudantes'
        verbose_name = 'Histórico do Estudante'
        verbose_name_plural = 'Históricos dos Estudantes'
        unique_together = ('estudante', 'projeto')
        ordering = ['-data_registro']

    def __str__(self):
        return f'{self.estudante} +{self.pontos}pts — {self.projeto}'
