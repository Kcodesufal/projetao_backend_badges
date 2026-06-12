from rest_framework import serializers

from autenticacao.enums.roles import Role
from autenticacao.serializers.usuario import UsuarioSerializer
from professores.models.professores import Professor
from professores.models.universidades import Universidade
from professores.serializers.universidade import UniversidadeSerializer


class ProfessorSerializer(serializers.ModelSerializer):
    usuario_detalhes = UsuarioSerializer(source='usuario', read_only=True)
    universidade_detalhes = UniversidadeSerializer(source='universidade', read_only=True)
    nome_universidade = serializers.CharField(write_only=True)

    class Meta:
        model = Professor
        fields = (
            'id',
            'usuario',
            'usuario_detalhes',
            'nome_universidade',
            'universidade_detalhes',
            'cpf',
            'data_nascimento',
            'telefone',
            'lattes',
            'data_criacao',
        )
        read_only_fields = ('id', 'data_criacao', 'usuario_detalhes', 'universidade_detalhes')
        extra_kwargs = {
            'usuario': {'write_only': True},
        }

    def validate_usuario(self, value):
        if value.role != Role.PROFESSOR:
            raise serializers.ValidationError('O usuário deve ter o perfil de Professor.')
        return value

    def create(self, validated_data):
        nome_universidade = validated_data.pop('nome_universidade')
        universidade, _ = Universidade.objects.get_or_create(nome=nome_universidade)
        return Professor.objects.create(universidade=universidade, **validated_data)


class AtualizarProfessorSerializer(serializers.ModelSerializer):
    nome_universidade = serializers.CharField(required=False)

    class Meta:
        model = Professor
        fields = ('nome_universidade', 'telefone', 'lattes', 'data_nascimento')

    def update(self, instance, validated_data):
        nome_universidade = validated_data.pop('nome_universidade', None)
        if nome_universidade:
            universidade, _ = Universidade.objects.get_or_create(nome=nome_universidade)
            instance.universidade = universidade
        return super().update(instance, validated_data)
