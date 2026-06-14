from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from badges.models.badge import Badge
from badges.serializers.badge import BadgeSerializer, BadgeCreateSerializer
from badges.permissions import IsProfessorOrEstudanteOrOngForView, CanEmitBadge

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BadgeCreateSerializer
        return BadgeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsProfessorOrEstudanteOrOngForView]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated, CanEmitBadge]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'estudante':
            return Badge.objects.filter(estudante__usuario=user)
        elif user.role == 'professor':
            estudante_id = self.request.query_params.get('estudante_id')
            if estudante_id:
                return Badge.objects.filter(estudante_id=estudante_id)
            return Badge.objects.all()
        elif user.role == 'ong':
            estudante_id = self.request.query_params.get('estudante_id')
            qs = Badge.objects.filter(emissor_ong__usuario=user)
            if estudante_id:
                return qs.filter(estudante_id=estudante_id)
            return qs
        return Badge.objects.none()
