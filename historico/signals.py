from django.db.models.signals import pre_save
from django.dispatch import receiver

from projetos.models.projeto import Projeto


@receiver(pre_save, sender=Projeto)
def projeto_concluido(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        anterior = Projeto.objects.get(pk=instance.pk)
    except Projeto.DoesNotExist:
        return

    status_mudou_para_concluido = (
        anterior.status != Projeto.Status.CONCLUIDO
        and instance.status == Projeto.Status.CONCLUIDO
    )

    if status_mudou_para_concluido:
        from historico.services import conceder_pontos_projeto
        conceder_pontos_projeto(instance)
