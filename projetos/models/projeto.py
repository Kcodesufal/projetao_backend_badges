from django.db import models

from ongs.models.ong import Ong


class Projeto(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = 'rascunho', 'Rascunho'
        ABERTO = 'aberto', 'Aberto'
        EM_ANDAMENTO = 'em_andamento', 'Em Andamento'
        CONCLUIDO = 'concluido', 'Concluído'
        CANCELADO = 'cancelado', 'Cancelado'

    ong = models.ForeignKey(
        Ong,
        on_delete=models.CASCADE,
        related_name='projetos',
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    objetivo = models.TextField()
    publico_alvo = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RASCUNHO)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    carga_horaria = models.PositiveIntegerField(help_text='Carga horária total em horas')
    vagas_turmas = models.PositiveIntegerField(default=1, help_text='Quantidade de turmas aceitas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projetos'
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.nome
