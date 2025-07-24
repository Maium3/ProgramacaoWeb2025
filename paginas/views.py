from django.views.generic import TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'
    
  
class UsuarioCreate(CreateView):
    model = Usuario
    fields = ['usuario','nome', 'data_nasc', 'email', 'nickname', 'codigo_id']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': 'Cadastrar Novo Usuário',
        'botao': 'Cadastrar'   
    }
     
class UniversoCreate(LoginRequiredMixin, CreateView):
    model = Universo 
    fields = ['nome','descricao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': 'Cadastrar Novo Usuário',
        'botao': 'Cadastrar'   
    }
    
class PersonagemCreate(LoginRequiredMixin, CreateView):
    model = Personagem 
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia', 'user']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
class ConversaCreate(LoginRequiredMixin, CreateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class MensagemCreate(LoginRequiredMixin, CreateView):
    model = Mensagem
    fields = ['enviada_por', 'enviada_em', 'conteudo', 'conversa_origem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class CombateCreate(LoginRequiredMixin, CreateView):
    model = Combate
    fields = ['conversa', 'mensagem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class UsuarioUpdate(LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['nome', 'data_nasc', 'email', 'nickname', 'codigo_id']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
class UniversoUpdate(LoginRequiredMixin, UpdateView):
    model = Universo 
    fields = ['nome','descricao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
class PersonagemUpdate(LoginRequiredMixin, UpdateView):
    model = Personagem 
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia', 'user']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
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


class UsuarioDelete(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class PersonagemDelete(LoginRequiredMixin, DeleteView):
    model = Personagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}


class ConversaDelete(LoginRequiredMixin, DeleteView):
    model = Conversa
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}


class MensagemDelete(LoginRequiredMixin, DeleteView):
    model = Mensagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
 

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