from rest_framework.permissions import BasePermission

from autenticacao.enums.roles import Role


class IsEstudante(BasePermission):
    message = 'Apenas estudantes podem realizar esta ação.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == Role.ESTUDANTE)
