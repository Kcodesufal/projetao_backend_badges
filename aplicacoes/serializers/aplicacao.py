from rest_framework import serializers

from aplicacoes.models.aplicacao import Aplicacao


class AplicacaoSerializer(serializers.ModelSerializer):
    turma_id = serializers.IntegerField(source='turma.id', read_only=True)
    professor_nome = serializers.CharField(source='professor.usuario.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)
    projeto_nome = serializers.CharField(source='atividade.projeto.nome', read_only=True)
    projeto_id = serializers.IntegerField(source='atividade.projeto.id', read_only=True)
    ong_id = serializers.IntegerField(source='atividade.projeto.ong.id', read_only=True)
    ong_nome = serializers.CharField(source='atividade.projeto.ong.razao_social', read_only=True)
    data_inicio = serializers.DateField(source='atividade.data_inicio', read_only=True)
    data_fim = serializers.DateField(source='atividade.data_fim', read_only=True)

    class Meta:
        model = Aplicacao
        fields = (
            'id',
            'professor',
            'professor_nome',
            'turma',
            'turma_id',
            'turma_nome',
            'atividade',
            'atividade_nome',
            'projeto_nome',
            'projeto_id',
            'ong_id',
            'ong_nome',
            'data_inicio',
            'data_fim',
            'justificativa',
            'status',
            'feedback_ong',
            'data_aplicacao',
            'data_atualizacao',
        )
        read_only_fields = (
            'id',
            'status',
            'feedback_ong',
            'data_aplicacao',
            'data_atualizacao',
            'professor_nome',
            'turma_id',
            'turma_nome',
            'atividade_nome',
            'projeto_nome',
            'projeto_id',
            'ong_id',
            'ong_nome',
            'data_inicio',
            'data_fim',
        )
        extra_kwargs = {}

    def validate(self, data):
        professor = data.get('professor')
        turma = data.get('turma')
        atividade = data.get('atividade')

        if turma and professor and turma.turmas_professor.filter(professor=professor).exists() is False:
            raise serializers.ValidationError('A turma não pertence ao professor informado.')

        if atividade and atividade.projeto.status not in ('aberto', 'em_andamento'):
            raise serializers.ValidationError('O projeto não está aberto para aplicações.')

        if Aplicacao.objects.filter(professor=professor, turma=turma, atividade=atividade).exists():
            raise serializers.ValidationError('Já existe uma aplicação para esta combinação.')

        return data


class AtualizarStatusAplicacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aplicacao
        fields = ('status', 'feedback_ong')

    def validate_status(self, value):
        if value == Aplicacao.Status.PENDENTE:
            raise serializers.ValidationError('Não é possível reverter para Pendente.')
        return value

    def validate(self, data):
        status_val = data.get('status')
        if not status_val or status_val != Aplicacao.Status.ACEITA:
            return data
            
        if self.instance and self.instance.status == Aplicacao.Status.ACEITA:
            return data
            
        atividade = self.instance.atividade
        projeto = atividade.projeto
        turma = self.instance.turma
        
        aplicacoes_aceitas_atividade = Aplicacao.objects.filter(
            atividade=atividade,
            status=Aplicacao.Status.ACEITA
        ).count()
        
        if aplicacoes_aceitas_atividade >= atividade.vagas:
            raise serializers.ValidationError(
                {'status': f'Limite de vagas ({atividade.vagas}) esgotado para a atividade {atividade.nome}.'}
            )
            
        turmas_aceitas_projeto = Aplicacao.objects.filter(
            atividade__projeto=projeto,
            status=Aplicacao.Status.ACEITA
        ).values('turma').distinct().count()
        
        ja_aceita_no_projeto = Aplicacao.objects.filter(
            atividade__projeto=projeto,
            turma=turma,
            status=Aplicacao.Status.ACEITA
        ).exists()
        
        if not ja_aceita_no_projeto and turmas_aceitas_projeto >= projeto.vagas_turmas:
            raise serializers.ValidationError(
                {'status': f'Limite de turmas ({projeto.vagas_turmas}) esgotado para o projeto {projeto.nome}.'}
            )
            
        return data
