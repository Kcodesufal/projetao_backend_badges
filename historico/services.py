from django.db import transaction

from aplicacoes.models.aplicacao import Aplicacao
from estudantes.models.estudantes_turmas import EstudanteTurma
from historico.models.historico import HistoricoEstudante
from historico.models.ranking import RankingEstudante


@transaction.atomic
def conceder_pontos_projeto(projeto):
    pontos = projeto.carga_horaria

    aplicacoes_aceitas = (
        Aplicacao.objects
        .filter(atividade__projeto=projeto, status=Aplicacao.Status.ACEITA)
        .select_related('turma')
        .distinct()
    )

    turmas_ids = aplicacoes_aceitas.values_list('turma_id', flat=True)

    estudantes_ids = (
        EstudanteTurma.objects
        .filter(turma_id__in=turmas_ids, status=EstudanteTurma.Status.ACEITO)
        .values_list('estudante_id', flat=True)
        .distinct()
    )

    for estudante_id in estudantes_ids:
        criado = HistoricoEstudante.objects.get_or_create(
            estudante_id=estudante_id,
            projeto=projeto,
            defaults={'pontos': pontos},
        )[1]

        if not criado:
            continue

        ranking, _ = RankingEstudante.objects.get_or_create(estudante_id=estudante_id)
        ranking.total_pontos += pontos
        ranking.atualizar_tier()
        ranking.save()
