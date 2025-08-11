
from django.contrib import admin
from django.urls import path
from .views import Inicio, SobreView, UsuarioCreate, UniversoCreate, PersonagemCreate, ConversaCreate, MensagemCreate, CombateCreate, UsuarioUpdate, UniversoUpdate, PersonagemUpdate, ConversaUpdate, UsuarioDelete, MensagemUpdate, PersonagemDelete, ConversaDelete, MensagemDelete
from .views import UsuarioList, UniversoList, PersonagemList, ConversaList, CombateList
from django.contrib.auth import views as auth_views
urlpatterns = [


    path('login/', auth_views.LoginView.as_view(
         template_name = 'paginas/form.html',
          extra_context = {
        'titulo': 'Login',
        'botao': 'login'   
    },
    ), name="Login"),

     path('alterar-senha/', auth_views.PasswordChangeView.as_view(
         template_name = 'paginas/form.html',
          extra_context = {
        'titulo': 'Atualizar senha',
        'botao': 'salvar'   
    },
    ), name="alterar senha"),
        
    path('sair/', auth_views.LogoutView.as_view(
         template_name = 'paginas/form.html',
          extra_context = {
        'titulo': 'Desconectar',
        'botao': 'Desconectar'   
    }
    ), name="Desconectar"),

    path("", Inicio.as_view(), name= "Inicio"),
    path('sobre-o-site/', SobreView.as_view(), name = "sobre"),
    path('cadastro-usuario/', UsuarioCreate.as_view(), name="cadastro_usuario"),
    path('cadastrar-universo/', UniversoCreate.as_view(), name="cadastro_de_universo"),
    path('criar-personagem/', PersonagemCreate.as_view(), name="criar_personagem"),
    path('iniciar-conversa/', ConversaCreate.as_view(), name="iniciar_conversa"),
    path('enviar-mensagem/', MensagemCreate.as_view(), name="enviar_mensagem"),
    path('iniciar-combate/', CombateCreate.as_view(), name="iniciar_novo_combate"),
    
    path('atualizar-usuario/<int:pk>/', UsuarioUpdate.as_view(), name="atualizar_usuario"),
    path('atualizar-universo/<int:pk>/', UniversoUpdate.as_view(), name="atualizar_universo"),
    path('alterar-personagem/<int:pk>/', PersonagemUpdate.as_view(), name="alterar_personagem"),
    path('modificar-conversa/<int:pk>/', ConversaUpdate.as_view(), name="modificar_conversa"),
    path('carregar-mensagem/<int:pk>/', MensagemUpdate.as_view(), name="carregar_mensagem"),
    
    path('deletar-usuario/<int:pk>/', UsuarioDelete.as_view(), name="deletar_usuario"),
    path('deletar-personagem/<int:pk>/', PersonagemDelete.as_view(), name="deletar_personagem"),
    path('excluir-conversa/<int:pk>/', ConversaDelete.as_view(), name="excluir_conversa"),
    path('excluir-mensagem/<int:pk>/', MensagemDelete.as_view(), name="excluir_mensagem"),

    path('listar-usuarios/', UsuarioList.as_view(), name="listar_usuarios"),
    path('listar-Universos/', UniversoList.as_view(), name="listar_Universos"),
    path('listar-personagens/', PersonagemList.as_view(), name="listar_personagens"),
    path('listar-conversa/', ConversaList.as_view(), name="listar_conversas"),
    path('listar-combates/', CombateList.as_view(), name="listar_Combates"),
    
]
