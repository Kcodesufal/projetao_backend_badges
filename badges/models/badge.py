from django.db import models
from estudantes.models.estudantes import Estudante
from professores.models.professores import Professor
from ongs.models.ong import Ong

class Badge(models.Model):
    TIPO_CHOICES = [
        ('Liderança', 'Liderança'),
        ('Trabalho em Equipe', 'Trabalho em Equipe'),
        ('Comunicação', 'Comunicação'),
        ('Organização', 'Organização'),
        ('Proatividade', 'Proatividade'),
        ('Impacto Social', 'Impacto Social'),
        ('Ensino e Capacitação', 'Ensino e Capacitação'),
        ('Inovação', 'Inovação'),
    ]

    NIVEL_CHOICES = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
    ]

    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='badges')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='I')
    descricao = models.TextField()
    justificativa = models.TextField()
    data_emissao = models.DateField(auto_now_add=True)
    
    emissor_professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True, related_name='badges_emitidas')
    emissor_ong = models.ForeignKey(Ong, on_delete=models.SET_NULL, null=True, blank=True, related_name='badges_emitidas')

    class Meta:
        db_table = 'badges'
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'

    def __str__(self):
        return f'{self.tipo} ({self.nivel}) - {self.estudante.usuario.first_name}'
