
from django.contrib import admin
from django.urls import path
from .views import Inicio, SobreView, UsuarioCreate, UniversoCreate, PersonagemCreate, ConversaCreate, MensagemCreate, CombateCreate

urlpatterns = [
    path("", Inicio.as_view(), name= "Inicio"),
    path('sobre-o-site/', SobreView.as_view(), name = "sobre"),
    path('cadastro-usuario/', UsuarioCreate.as_view(), name="cadastro_usuario"),
    path('cadastrar-universo/', UniversoCreate.as_view(), name="cadastro_de_universo"),
    path('criar-personagem/', PersonagemCreate.as_view(), name="criar_personagem"),
    path('iniciar-conversa/', ConversaCreate.as_view(), name="iniciar_conversa"),
    path('enviar-mensagem/', MensagemCreate.as_view(), name="enviar_mensagem"),
    path('iniciar-combate/', CombateCreate.as_view(), name="iniciar_novo_combate")
    
]
