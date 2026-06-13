from django.db import models

from projetos.models.projeto import Projeto


class Atividade(models.Model):
    class Tipo(models.TextChoices):
        PRATICA = 'pratica', 'Prática'
        TEORICA = 'teorica', 'Teórica'
        WORKSHOP = 'workshop', 'Workshop'
        PESQUISA = 'pesquisa', 'Pesquisa'
        EXTENSAO = 'extensao', 'Extensão'

    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='atividades',
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    carga_horaria = models.PositiveIntegerField(help_text='Carga horária da atividade em horas')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    vagas = models.PositiveIntegerField(default=1, help_text='Quantidade de turmas aceitas nesta atividade')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'atividades'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['data_inicio']

    def __str__(self):
        return f'{self.nome} — {self.projeto}'
