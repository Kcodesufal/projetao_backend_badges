from django.urls import path

from autenticacao.views.login import LoginView
from autenticacao.views.cadastro import CadastroView
from autenticacao.views.trocar_senha import TrocarSenhaView
from autenticacao.views.usuario import UsuarioListView, UsuarioRetrieveView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('trocar-senha/', TrocarSenhaView.as_view(), name='trocar-senha'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),
    path('usuarios/<int:pk>/', UsuarioRetrieveView.as_view(), name='usuario-retrieve'),
]
