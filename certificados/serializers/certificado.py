from rest_framework import serializers

from certificados.models.certificado import Certificado


class CertificadoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.CharField(source='estudante.usuario.get_full_name', read_only=True)
    estudante_matricula = serializers.CharField(source='estudante.matricula', read_only=True)
    estudante_curso = serializers.CharField(source='estudante.curso', read_only=True)
    universidade_nome = serializers.CharField(source='estudante.universidade.nome', read_only=True)
    projeto_nome = serializers.CharField(source='projeto.nome', read_only=True)
    projeto_ong = serializers.CharField(source='projeto.ong.nome', read_only=True)
    projeto_data_inicio = serializers.DateField(source='projeto.data_inicio', read_only=True)
    projeto_data_fim = serializers.DateField(source='projeto.data_fim', read_only=True)

    class Meta:
        model = Certificado
        fields = (
            'id',
            'codigo_verificacao',
            'estudante',
            'estudante_nome',
            'estudante_matricula',
            'estudante_curso',
            'universidade_nome',
            'projeto',
            'projeto_nome',
            'projeto_ong',
            'projeto_data_inicio',
            'projeto_data_fim',
            'carga_horaria',
            'data_emissao',
        )
        read_only_fields = fields


class EmitirCertificadoSerializer(serializers.Serializer):
    projeto_id = serializers.IntegerField()
