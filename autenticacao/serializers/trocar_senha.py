from rest_framework import serializers


class TrocarSenhaSerializer(serializers.Serializer):
    senha_atual = serializers.CharField(write_only=True)
    senha_nova = serializers.CharField(write_only=True, min_length=8)

    def validate_senha_atual(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Senha atual incorreta.')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['senha_nova'])
        user.save()
