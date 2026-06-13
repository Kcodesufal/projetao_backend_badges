from rest_framework import serializers

from professores.models.professores import Professor
from professores.serializers.universidade import UniversidadeSerializer
from turmas.models.turmas import Turma
from turmas.models.turmas_professor import TurmaProfessor


class TurmaSerializer(serializers.ModelSerializer):
    universidade_detalhes = UniversidadeSerializer(source='universidade', read_only=True)

    class Meta:
        model = Turma
        fields = (
            'id',
            'nome',
            'descricao',
            'universidade',
            'universidade_detalhes',
            'periodo',
            'modalidade',
            'semestre',
            'vagas',
            'ativa',
            'data_criacao',
        )
        read_only_fields = ('id', 'data_criacao', 'universidade_detalhes')
        extra_kwargs = {
            'universidade': {'write_only': True},
        }

    def validate(self, data):
        request = self.context['request']
        try:
            professor = Professor.objects.get(usuario=request.user)
        except Professor.DoesNotExist:
            raise serializers.ValidationError('Usuário não possui perfil de professor.')

        universidade = data.get('universidade')
        if universidade and professor.universidade != universidade:
            raise serializers.ValidationError(
                'A universidade da turma deve ser a mesma do professor.'
            )

        self.context['professor'] = professor
        return data

    def create(self, validated_data):
        professor = self.context['professor']
        turma = Turma.objects.create(**validated_data)
        TurmaProfessor.objects.create(professor=professor, turma=turma)
        return turma


class AtualizarTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ('nome', 'descricao', 'periodo', 'modalidade', 'semestre', 'vagas', 'ativa')


class MinhasTurmasSerializer(serializers.ModelSerializer):
    universidade = UniversidadeSerializer(read_only=True)
    total_vinculos = serializers.SerializerMethodField()

    class Meta:
        model = Turma
        fields = (
            'id',
            'nome',
            'descricao',
            'universidade',
            'periodo',
            'modalidade',
            'semestre',
            'vagas',
            'ativa',
            'total_vinculos',
            'data_criacao',
        )

    def get_total_vinculos(self, obj):
        return obj.turmas_professor.count()
