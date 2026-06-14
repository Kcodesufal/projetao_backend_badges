from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from badges.models.badge import Badge
from badges.serializers.badge import BadgeSerializer, BadgeCreateSerializer
from badges.permissions import IsProfessorOrEstudanteForView, CanEmitBadge

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BadgeCreateSerializer
        return BadgeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsProfessorOrEstudanteForView]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, CanEmitBadge]
        else:
            permission_classes = [IsAuthenticated] # Or some specific admin permission
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'estudante':
            return Badge.objects.filter(estudante__usuario=user)
        elif user.role == 'professor':
            # Professor pode ver os badges de qualquer estudante (ou apenas dos estudantes que acessam, aqui retornamos todos)
            estudante_id = self.request.query_params.get('estudante_id')
            if estudante_id:
                return Badge.objects.filter(estudante_id=estudante_id)
            return Badge.objects.all()
        # Se for ONG ou outro (que não deveria ter acesso de view por causa das permissoes, mas por seguranca retornamos none)
        return Badge.objects.none()
