from django.db import models

from professores.models.universidades import Universidade


class Turma(models.Model):
    class Periodo(models.TextChoices):
        MANHA = 'manha', 'Manhã'
        TARDE = 'tarde', 'Tarde'
        NOITE = 'noite', 'Noite'
        INTEGRAL = 'integral', 'Integral'

    class Modalidade(models.TextChoices):
        PRESENCIAL = 'presencial', 'Presencial'
        REMOTO = 'remoto', 'Remoto'
        HIBRIDO = 'hibrido', 'Híbrido'

    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, default='')
    universidade = models.ForeignKey(
        Universidade,
        on_delete=models.PROTECT,
        related_name='turmas',
    )
    periodo = models.CharField(max_length=20, choices=Periodo.choices)
    modalidade = models.CharField(max_length=20, choices=Modalidade.choices, default=Modalidade.PRESENCIAL)
    semestre = models.CharField(max_length=10, help_text='Ex: 2025.1')
    vagas = models.PositiveIntegerField(default=0)
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'turmas'
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

    def __str__(self):
        return f'{self.nome} — {self.semestre}'
