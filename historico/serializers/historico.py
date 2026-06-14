from rest_framework import serializers

from historico.models.historico import HistoricoEstudante


class HistoricoEstudanteSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.nome', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)
    projeto_carga_horaria = serializers.IntegerField(source='projeto.carga_horaria', read_only=True)

    class Meta:
        model = HistoricoEstudante
        fields = (
            'id',
            'estudante',
            'estudante_nome',
            'projeto',
            'projeto_nome',
            'projeto_carga_horaria',
            'pontos',
            'data_registro',
        )
        read_only_fields = fields
