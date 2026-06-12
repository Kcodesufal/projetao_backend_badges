from django.db import models


class CausaSocial(models.TextChoices):
    EDUCACAO = 'educacao', 'Educação'
    SAUDE = 'saude', 'Saúde'
    MEIO_AMBIENTE = 'meio_ambiente', 'Meio Ambiente'
    DIREITOS_HUMANOS = 'direitos_humanos', 'Direitos Humanos'
    ASSISTENCIA_SOCIAL = 'assistencia_social', 'Assistência Social'
    CULTURA = 'cultura', 'Cultura e Arte'
    ESPORTE = 'esporte', 'Esporte'
    TECNOLOGIA = 'tecnologia', 'Tecnologia e Inovação'
