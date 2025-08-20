from django.views.generic import TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate, Favoritos


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin




class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'
    
  
class UsuarioCreate(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['nome', 'data_nasc']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário criado com sucesso"
    extra_context = {
        'titulo': 'Cadastrar Novo Usuário',
        'botao': 'Cadastrar'   
    }
     
class UniversoCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Universo 
    fields = ['nome','descricao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_Universos')
    success_message = "Universo criado com sucesso"
    extra_context = {
        'titulo': 'Cadastrar Novo Universo',
        'botao': 'Cadastrar'   
    }
    
class PersonagemCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Personagem 
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia', 'user']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Personagem criado com sucesso"
    extra_context = {}
    
class ConversaCreate(LoginRequiredMixin, CreateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "iniciar nova conversa",
        'botao': "Iniciar"

    }

class MensagemCreate(LoginRequiredMixin, CreateView):
    model = Mensagem
    fields = ['enviada_por', 'enviada_em', 'conteudo', 'conversa_origem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "Enviar mensagem",
        'botao': "Enviar"

    }

class CombateCreate(LoginRequiredMixin, CreateView):
    model = Combate
    fields = ['conversa', 'mensagem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class FavoritoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Favoritos
    fields = ['amigo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário adcionado com sucesso"
    extra_context = {
        'titulo': 'Salvar novo contato',
        'botao': 'Salvar'   
    }



class UsuarioUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['nome', 'data_nasc']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário foi atualizado com sucesso"
    extra_context = {
        'titulo': 'Atualuzar meus dados',
        'botao': 'Confirmar'   
    }
    
class UniversoUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Universo 
    fields = ['nome','descricao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_Universos')
    success_message = "Universo foi atualizado com sucesso"
    extra_context = {
        'titulo': 'Atualizar Universo',
        'botao': 'Salvar'   
    }
    

class PersonagemUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Personagem 
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia', 'user']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    
    success_message = "O Personagem %(nome)% foi atualizado com sucesso"
    extra_context = {}

class ConversaUpdate(LoginRequiredMixin, UpdateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

    
class MensagemUpdate(LoginRequiredMixin, UpdateView):
    model = Mensagem
    fields = ['enviada_por', 'enviada_em', 'conteudo', 'conversa_origem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}


class UsuarioDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário foi deletado com sucesso"
    extra_context = {}

class PersonagemDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Personagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "O Personagem %(nome)% foi deletado com sucesso"
    extra_context = {}


class ConversaDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Conversa
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Conversa deletada com sucesso"
    extra_context = {}


class MensagemDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Mensagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Mensagem deletada com sucesso"
    extra_context = {}

class FavoritoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Favoritos
    fields = ['amigo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário excluido com sucesso"
    extra_context = {
        'titulo': 'Excluir contato',
        'botao': 'Excluir'   
    }
 

class UsuarioList(LoginRequiredMixin, ListView):
    model= Usuario
    template_name = "paginas/usuario.html"


class UniversoList(ListView):
    model= Universo
    template_name = "paginas/universo.html"


class PersonagemList(ListView):
    model= Personagem
    template_name = "paginas/pesonagem.html"


class ConversaList(LoginRequiredMixin, ListView):
    model= Conversa
    template_name = "paginas/conversa.html" 


class CombateList(ListView):
    model= Combate
    template_name = "paginas/usuario.html" 

class FavoritoList(ListView):
    model= Favoritos
    template_name= "paginas/favoritos.html"