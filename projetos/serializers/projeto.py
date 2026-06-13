from rest_framework import serializers

from ongs.models.ong import Ong
from projetos.models.projeto import Projeto


class ProjetoSerializer(serializers.ModelSerializer):
    ong_nome = serializers.CharField(source='ong.razao_social', read_only=True)

    class Meta:
        model = Projeto
        fields = (
            'id',
            'ong',
            'ong_nome',
            'nome',
            'descricao',
            'objetivo',
            'publico_alvo',
            'status',
            'data_inicio',
            'data_fim',
            'carga_horaria',
            'vagas_turmas',
            'data_criacao',
            'data_atualizacao',
        )
        read_only_fields = ('id', 'data_criacao', 'data_atualizacao', 'ong_nome')
        extra_kwargs = {'ong': {'write_only': True}}

    def validate(self, data):
        if data.get('data_fim') and data.get('data_inicio'):
            if data['data_fim'] <= data['data_inicio']:
                raise serializers.ValidationError('A data de fim deve ser posterior à data de início.')
        return data


class AtualizarProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = ('nome', 'descricao', 'objetivo', 'publico_alvo', 'status', 'data_inicio', 'data_fim', 'carga_horaria', 'vagas_turmas')

    def validate(self, data):
        instance = self.instance
        data_inicio = data.get('data_inicio', instance.data_inicio)
        data_fim = data.get('data_fim', instance.data_fim)
        if data_fim <= data_inicio:
            raise serializers.ValidationError('A data de fim deve ser posterior à data de início.')
        return data
