from rest_framework import serializers
from badges.models.badge import Badge

class BadgeSerializer(serializers.ModelSerializer):
    emissor_nome = serializers.SerializerMethodField()
    emissor_tipo = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = [
            'id', 'estudante', 'tipo', 'nivel', 'descricao', 
            'justificativa', 'data_emissao', 'emissor_nome', 'emissor_tipo', 'aplicacao'
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
            'estudante', 'tipo', 'nivel', 'descricao', 'justificativa', 'aplicacao'
        ]

    def validate(self, data):
        user = self.context['request'].user
        if user.role == 'ong':
            aplicacao = data.get('aplicacao')
            if not aplicacao:
                raise serializers.ValidationError({'aplicacao': 'A ONG deve informar a aplicação associada ao badge.'})
            
            if aplicacao.atividade.projeto.ong.usuario != user:
                raise serializers.ValidationError('Você não é a ONG responsável por esta aplicação.')
            
            estudante = data.get('estudante')
            from estudantes.models.estudantes_turmas import EstudanteTurma
            is_aceito = EstudanteTurma.objects.filter(
                estudante=estudante,
                turma=aplicacao.turma,
                status=EstudanteTurma.Status.ACEITO
            ).exists()
            
            if not is_aceito:
                raise serializers.ValidationError('O estudante não está inscrito ou aceito na turma desta aplicação.')
            
            # Verificar se o estudante não foi rejeitado pela ONG
            if aplicacao.estudantes_rejeitados.filter(id=estudante.id).exists():
                raise serializers.ValidationError('Este estudante foi removido desta atividade pela ONG.')
                
        return data

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
