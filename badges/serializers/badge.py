from rest_framework import serializers
from badges.models.badge import Badge

class BadgeSerializer(serializers.ModelSerializer):
    emissor_nome = serializers.SerializerMethodField()
    emissor_tipo = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = [
            'id', 'estudante', 'tipo', 'nivel', 'descricao', 
            'justificativa', 'data_emissao', 'emissor_nome', 'emissor_tipo'
        ]
        read_only_fields = ['data_emissao', 'emissor_nome', 'emissor_tipo']

    def get_emissor_nome(self, obj):
        if obj.emissor_ong:
            return obj.emissor_ong.razao_social
        if obj.emissor_professor:
            return f"{obj.emissor_professor.usuario.first_name} {obj.emissor_professor.usuario.last_name}".strip()
        return "Sistema"

    def get_emissor_tipo(self, obj):
        if obj.emissor_ong:
            return "ONG"
        if obj.emissor_professor:
            return "Professor"
        return "Sistema"

class BadgeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = [
            'estudante', 'tipo', 'nivel', 'descricao', 'justificativa'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        
        if user.role == 'ong':
            from ongs.models.ong import Ong
            try:
                validated_data['emissor_ong'] = Ong.objects.get(usuario=user)
            except Ong.DoesNotExist:
                pass
        elif user.role == 'professor':
            from professores.models.professores import Professor
            try:
                validated_data['emissor_professor'] = Professor.objects.get(usuario=user)
            except Professor.DoesNotExist:
                pass
            
        return super().create(validated_data)
