from rest_framework import serializers

from aplicacoes.models.aplicacao import Aplicacao


class AplicacaoSerializer(serializers.ModelSerializer):
    professor_nome = serializers.CharField(source='professor.usuario.nome', read_only=True)
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    atividade_nome = serializers.CharField(source='atividade.nome', read_only=True)
    projeto_nome = serializers.CharField(source='atividade.projeto.nome', read_only=True)
    projeto_id = serializers.IntegerField(source='atividade.projeto.id', read_only=True)
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
            'turma_nome',
            'atividade',
            'atividade_nome',
            'projeto_nome',
            'projeto_id',
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
            'turma_nome',
            'atividade_nome',
            'projeto_nome',
            'projeto_id',
            'ong_nome',
            'data_inicio',
            'data_fim',
        )
        extra_kwargs = {
            'professor': {'write_only': True},
            'turma': {'write_only': True},
            'atividade': {'write_only': True},
        }

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
