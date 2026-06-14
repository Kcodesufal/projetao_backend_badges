from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver([post_save, post_delete], sender='ongs.AvaliacaoOng')
def recalcular_avaliacao_ong(sender, instance, **kwargs):
    from ongs.models.ong import Ong

    resultado = instance.ong.avaliacoes.aggregate(media=Avg('nota'))
    media = resultado['media']

    Ong.objects.filter(pk=instance.ong_id).update(
        avaliacao_media=round(media, 1) if media is not None else None
    )
