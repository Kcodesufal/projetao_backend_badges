from django.db import models


class Tier(models.TextChoices):
    BRONZE = 'bronze', 'Bronze'
    PRATA = 'prata', 'Prata'
    OURO = 'ouro', 'Ouro'
    PLATINA = 'platina', 'Platina'
    ESMERALDA = 'esmeralda', 'Esmeralda'
    DIAMANTE = 'diamante', 'Diamante'
    MESTRE = 'mestre', 'Mestre'
    GRAO_MESTRE = 'grao_mestre', 'Grão-Mestre'
    DESAFIANTE = 'desafiante', 'Desafiante'


TIER_THRESHOLDS = [
    (800, Tier.DESAFIANTE),
    (700, Tier.GRAO_MESTRE),
    (600, Tier.MESTRE),
    (500, Tier.DIAMANTE),
    (400, Tier.ESMERALDA),
    (300, Tier.PLATINA),
    (200, Tier.OURO),
    (100, Tier.PRATA),
    (0,   Tier.BRONZE),
]


def calcular_tier(total_pontos: int) -> str:
    for minimo, tier in TIER_THRESHOLDS:
        if total_pontos >= minimo:
            return tier
    return Tier.BRONZE
