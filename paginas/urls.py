
from django.contrib import admin
from django.urls import path
from .views import Inicio, SobreView
from .views import UsuarioCreate, UniversoCreate, PersonagemCreate, ConversaCreate, MensagemCreate, CombateCreate, FavoritoCreate
from .views import UsuarioUpdate, UniversoUpdate, PersonagemUpdate, ConversaUpdate, MensagemUpdate
from .views import UsuarioDelete, PersonagemDelete, ConversaDelete, MensagemDelete, FavoritoDelete, UniversoDelete
from .views import UsuarioList, UniversoList, PersonagemList, ConversaList, MensagemList, CombateList, FavoritoList
from .views import MeusPersonagens, ConversaDetailView, MinhasConversasList, MinhasMensagensList
from .views import ConversaUsuariosList, ConversaUsuariosDetailView, ConversaUsuariosCreate, MensagemConversaUsuariosCreate, ConversaUsuariosFromFavorito
from django.contrib.auth import views as auth_views
from .views import CadastroUsuarioView


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

    path("registrar/", CadastroUsuarioView.as_view(), name="registrar"),

    path("", Inicio.as_view(), name= "Inicio"),
    path('sobre-o-site/', SobreView.as_view(), name = "sobre"),
    path('cadastro-usuario/', UsuarioCreate.as_view(), name="cadastro_usuario"),
    path('cadastrar-universo/', UniversoCreate.as_view(), name="cadastro_de_universo"),
    path('criar-personagem/', PersonagemCreate.as_view(), name="criar_personagem"),
    path('iniciar-conversa/', ConversaCreate.as_view(), name="iniciar_conversa"),
    path('enviar-mensagem/', MensagemCreate.as_view(), name="enviar_mensagem"),
    path('iniciar-combate/', CombateCreate.as_view(), name="iniciar_novo_combate"),
    path('adcionar-favorito/', FavoritoCreate.as_view(), name="adcionar_aos_contatos"),
    
    path('atualizar/usuario/<int:pk>/', UsuarioUpdate.as_view(), name="atualizar_usuario"),
    path('atualizar/universo/<int:pk>/', UniversoUpdate.as_view(), name="atualizar_universo"),
    path('atualizar/personagem/<int:pk>/', PersonagemUpdate.as_view(), name="alterar_personagem"),
    path('atualizar/conversa/<int:pk>/', ConversaUpdate.as_view(), name="atualizar_conversa"),
    path('atualizar/mensagem/<int:pk>/', MensagemUpdate.as_view(), name="carregar_mensagem"),
    
    path('excluir-usuario/<int:pk>/', UsuarioDelete.as_view(), name="deletar_usuario"),
    path('excluir-universo/<int:pk>/', UniversoDelete.as_view(), name="excluir_universo"),
    path('excluir-personagem/<int:pk>/', PersonagemDelete.as_view(), name="deletar_personagem"),
    path('excluir-conversa/<int:pk>/', ConversaDelete.as_view(), name="excluir_conversa"),
    path('excluir-mensagem/<int:pk>/', MensagemDelete.as_view(), name="excluir_mensagem"),
    path('excluir-contato/<int:pk>/', FavoritoDelete.as_view(), name="excluir_contato"),

    path('listar/usuarios/', UsuarioList.as_view(), name="listar_usuarios"),
    path('listar/Universos/', UniversoList.as_view(), name="listar_Universos"),
    path('listar/personagens/', PersonagemList.as_view(), name="listar_personagens"),
    path('listar/conversa/', ConversaList.as_view(), name="listar_conversas"),
    path('listar/conversa/<int:universo_id>/', ConversaList.as_view(), name="listar_conversas"),
    path('listar/mensagens/', MensagemList.as_view(), name="listar_mensagens"),
    path('listar/combates/', CombateList.as_view(), name="listar_Combates"),
    path('lista/favoritos/', FavoritoList.as_view(), name="listar_contatos"),
    path('minhas-conversas/', MinhasConversasList.as_view(), name="minhas_conversas"),
    path('minhas-mensagens/', MinhasMensagensList.as_view(), name="minhas_mensagens"),

  # Conversas privadas entre usuários
  path('listar/conversa-usuarios/', ConversaUsuariosList.as_view(), name='listar_conversas_usuarios'),
  path('iniciar-conversa-usuario/', ConversaUsuariosCreate.as_view(), name='iniciar_conversa_usuario'),
  path('conversa-usuario/<int:pk>/', ConversaUsuariosDetailView.as_view(), name='detalhe_conversa_usuarios'),
  path('conversa-usuario/<int:pk>/enviar/', MensagemConversaUsuariosCreate.as_view(), name='enviar_mensagem_conversa_usuarios'),

    path('conversa/<int:pk>/', ConversaDetailView.as_view(), name="detalhe_conversa"),

  # ConversaUsuarios via favorito
  path('iniciar-conversa-por-favorito/<int:pk>/', ConversaUsuariosFromFavorito.as_view(), name='iniciar_conversa_por_favorito'),

    path('listar/meus-personagens/', MeusPersonagens.as_view(), name="listando_personagens")
    
]
