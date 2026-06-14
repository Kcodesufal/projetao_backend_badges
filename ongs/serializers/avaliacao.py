from rest_framework import serializers

from ongs.models.avaliacao import AvaliacaoOng


class AvaliacaoOngSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.get_full_name', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)

    class Meta:
        model = AvaliacaoOng
        fields = (
            'id',
            'estudante',
            'estudante_nome',
            'ong',
            'projeto',
            'projeto_nome',
            'nota',
            'comentario',
            'data_avaliacao',
        )
        read_only_fields = ('id', 'estudante', 'estudante_nome', 'projeto_nome', 'data_avaliacao')


class AvaliarOngSerializer(serializers.Serializer):
    projeto_id = serializers.IntegerField()
    nota = serializers.DecimalField(max_digits=3, decimal_places=1, min_value=0, max_value=10)
    comentario = serializers.CharField(required=False, allow_blank=True, default='')
