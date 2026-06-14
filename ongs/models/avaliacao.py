from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from estudantes.models.estudantes import Estudante
from ongs.models.ong import Ong
from projetos.models.projeto import Projeto


class AvaliacaoOng(models.Model):
    estudante = models.ForeignKey(
        Estudante,
        on_delete=models.CASCADE,
        related_name='avaliacoes_ongs',
    )
    ong = models.ForeignKey(
        Ong,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='avaliacoes_ong',
    )
    nota = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Nota de 0 a 10',
    )
    comentario = models.TextField(blank=True, default='')
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'avaliacoes_ongs'
        verbose_name = 'Avaliação de ONG'
        verbose_name_plural = 'Avaliações de ONGs'
        unique_together = ('estudante', 'projeto')
        ordering = ['-data_avaliacao']

    def __str__(self):
        return f'{self.estudante} avaliou {self.ong} ({self.nota}) — {self.projeto}'
