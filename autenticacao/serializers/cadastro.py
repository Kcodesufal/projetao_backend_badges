from rest_framework import serializers

from autenticacao.enums.roles import Role
from autenticacao.models.user import Usuario


class CadastroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=Role.choices, default=Role.ESTUDANTE)

    class Meta:
        model = Usuario
        fields = ('email', 'nome', 'password', 'role')

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
