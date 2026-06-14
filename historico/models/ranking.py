from django.db import models

from estudantes.models.estudantes import Estudante
from historico.enums.tier import Tier, calcular_tier


class RankingEstudante(models.Model):
    estudante = models.OneToOneField(
        Estudante,
        on_delete=models.CASCADE,
        related_name='ranking',
    )
    total_pontos = models.PositiveIntegerField(default=0)
    tier = models.CharField(max_length=20, choices=Tier.choices, default=Tier.BRONZE)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ranking_estudantes'
        verbose_name = 'Ranking do Estudante'
        verbose_name_plural = 'Ranking dos Estudantes'
        ordering = ['-total_pontos']

    def atualizar_tier(self):
        self.tier = calcular_tier(self.total_pontos)

    def __str__(self):
        return f'{self.estudante} — {self.tier} ({self.total_pontos}pts)'
