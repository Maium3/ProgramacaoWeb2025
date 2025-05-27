
from django.contrib import admin
from django.urls import path
from .views import Inicio, SobreView, UsuarioCreate, UniversoCreate, PersonagemCreate, ConversaCreate, MensagemCreate, CombateCreate, UsuarioUpdate, UniversoUpdate, PersonagemUpdate, ConversaUpdate, MensagemUpdate, PersonagemDelete, ConversaDelete, MensagemDelete, CombateDelete

urlpatterns = [
    path("", Inicio.as_view(), name= "Inicio"),
    path('sobre-o-site/', SobreView.as_view(), name = "sobre"),
    path('cadastro-usuario/', UsuarioCreate.as_view(), name="cadastro_usuario"),
    path('cadastrar-universo/', UniversoCreate.as_view(), name="cadastro_de_universo"),
    path('criar-personagem/', PersonagemCreate.as_view(), name="criar_personagem"),
    path('iniciar-conversa/', ConversaCreate.as_view(), name="iniciar_conversa"),
    path('enviar-mensagem/', MensagemCreate.as_view(), name="enviar_mensagem"),
    path('iniciar-combate/', CombateCreate.as_view(), name="iniciar_novo_combate"),
    
    path('atualizar-usuario/', UsuarioUpdate.as_view(), name="atualizar_usuario"),
    path('atualizar-universo/', UniversoUpdate.as_view(), name="atualizar_universo"),
    path('alterar-personagem/', PersonagemUpdate.as_view(), name="alterar_personagem"),
    path('modificar-conversa/', ConversaUpdate.as_view(), name="modificar_conversa"),
    path('carregar-mensagem/', MensagemUpdate.as_view(), name="carregar_mensagem"),
    
    path('deletar-usuario/', UsuarioDelete.as_view(), name="deletar_usuario"),
    path('deletar-personagem/', PersonagemDelete.as_view(), name="deletar_personagem"),
    path('excluir-conversa/', ConversaDelete.as_view(), name="excluir_conversa"),
    path('excluir-mensagem/', MensagemUpdate.as_view(), name="excluir_mensagem"),
    path('apagar-combate/', CombateDelete.as_view(), name="apagar_combate")
    
]
