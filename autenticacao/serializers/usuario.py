from rest_framework import serializers

from autenticacao.models.user import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'nome', 'role', 'is_active', 'data_criacao')
        read_only_fields = fields
