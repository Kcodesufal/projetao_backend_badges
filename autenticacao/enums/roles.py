from django.db import models


class Role(models.TextChoices):
    VOLUNTARIO_INDEPENDENTE = 'voluntario_independente', 'Voluntário Independente'
    ESTUDANTE = 'estudante', 'Estudante'
    PROFESSOR = 'professor', 'Professor'
    ONG = 'ong', 'ONG'
    ADMINISTRADOR = 'administrador', 'Administrador'
