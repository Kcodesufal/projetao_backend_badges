from rest_framework.permissions import BasePermission

from autenticacao.enums.roles import Role

class IsProfessorOrEstudanteOrOngForView(BasePermission):
    message = 'Apenas professores, estudantes e ONGs podem visualizar badges.'

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return bool(request.user and request.user.is_authenticated and request.user.role in [Role.PROFESSOR, Role.ESTUDANTE, Role.ONG])
        return True

class CanEmitBadge(BasePermission):
    message = 'Apenas professores e ONGs podem emitir badges.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated and request.user.role in [Role.PROFESSOR, Role.ONG])
        return True
