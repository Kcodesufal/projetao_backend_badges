from rest_framework import serializers

from estudantes.models.estudantes import Estudante
from estudantes.models.estudantes_turmas import EstudanteTurma
from turmas.models.turmas import Turma


class InscricaoTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudanteTurma
        fields = ('id', 'estudante', 'turma', 'status', 'data_inscricao', 'data_atualizacao')
        read_only_fields = ('id', 'status', 'data_inscricao', 'data_atualizacao')

    def validate(self, data):
        estudante = data['estudante']
        turma = data['turma']

        if not turma.ativa:
            raise serializers.ValidationError('Esta turma não está ativa.')

        if EstudanteTurma.objects.filter(estudante=estudante, turma=turma).exists():
            raise serializers.ValidationError('Estudante já está inscrito nesta turma.')

        return data


class InscricaoDetalheSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    universidade_nome = serializers.CharField(source='turma.universidade.nome', read_only=True)

    class Meta:
        model = EstudanteTurma
        fields = (
            'id',
            'estudante',
            'estudante_nome',
            'turma',
            'turma_nome',
            'universidade_nome',
            'status',
            'data_inscricao',
            'data_atualizacao',
        )
        read_only_fields = fields


class AtualizarStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstudanteTurma
        fields = ('status',)

    def validate_status(self, value):
        if value == EstudanteTurma.Status.PRE_APROVADO:
            raise serializers.ValidationError('Não é possível reverter para Pré Aprovado.')
        return value
