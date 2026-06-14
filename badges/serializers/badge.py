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
        
        # Atribuir o emissor baseado no role do usuário logado
        if user.role == 'ong':
            validated_data['emissor_ong'] = user.ongs.first() # Supondo related_name
        elif user.role == 'professor':
            validated_data['emissor_professor'] = user.professores.first() # Supondo related_name
            
        return super().create(validated_data)
