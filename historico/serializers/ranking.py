from rest_framework import serializers

from historico.enums.tier import TIER_THRESHOLDS
from historico.models.ranking import RankingEstudante


class RankingEstudanteSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.nome', read_only=True)
    universidade = serializers.CharField(source='estudante.universidade.nome', read_only=True)
    pontos_proximo_tier = serializers.SerializerMethodField()

    class Meta:
        model = RankingEstudante
        fields = (
            'id',
            'estudante',
            'estudante_nome',
            'universidade',
            'total_pontos',
            'tier',
            'pontos_proximo_tier',
            'data_atualizacao',
        )
        read_only_fields = fields

    def get_pontos_proximo_tier(self, obj):
        for minimo, _ in reversed(TIER_THRESHOLDS):
            if minimo > obj.total_pontos:
                return minimo - obj.total_pontos
        return 0
