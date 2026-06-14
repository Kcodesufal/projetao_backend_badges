from rest_framework import serializers

from atividades.models.atividade import Atividade


class AtividadeSerializer(serializers.ModelSerializer):
    projeto_id = serializers.IntegerField(source='projeto.id', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)

    class Meta:
        model = Atividade
        fields = (
            'id',
            'projeto',
            'projeto_id',
            'projeto_nome',
            'nome',
            'descricao',
            'tipo',
            'carga_horaria',
            'data_inicio',
            'data_fim',
            'vagas',
            'data_criacao',
        )
        read_only_fields = ('id', 'data_criacao', 'projeto_id', 'projeto_nome')
        extra_kwargs = {'projeto': {'write_only': True}}

    def validate(self, data):
        if data.get('data_fim') and data.get('data_inicio'):
            if data['data_fim'] <= data['data_inicio']:
                raise serializers.ValidationError('A data de fim deve ser posterior à data de início.')
        return data


class AtualizarAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = ('nome', 'descricao', 'tipo', 'carga_horaria', 'data_inicio', 'data_fim', 'vagas')

    def validate(self, data):
        instance = self.instance
        data_inicio = data.get('data_inicio', instance.data_inicio)
        data_fim = data.get('data_fim', instance.data_fim)
        if data_fim <= data_inicio:
            raise serializers.ValidationError('A data de fim deve ser posterior à data de início.')
        return data
