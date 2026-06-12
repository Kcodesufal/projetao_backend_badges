from rest_framework import serializers

from professores.models.universidades import Universidade


class UniversidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidade
        fields = ('id', 'nome')
        read_only_fields = ('id',)


class AtualizarUniversidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universidade
        fields = ('nome',)
