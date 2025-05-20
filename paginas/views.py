from django.views.generic import *
from django.views.generic.edit import CreateView
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate

from django.urls import reverse_lazy

class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'
    
  
class UsuarioCreate(CreateView):
    model = Usuario
    fields = ['nome', 'data_nasc', 'email', 'nickname', 'id']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
class UsuarioUpdate(UpdateView):
     model = Usuario
     fields = ['nome', 'data_nasc', 'email', 'nickname', 'id']
     template_name = 'paginas/form.html'
     success_url = reverse_lazy('Inicio')
     extra_context = {}
     
class UniversoCreate(CreateView):
    model = Universo 
    fields = ['nome','descricao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
    
class UniversoUpdate(UpdateView):
    model = Universo
    template_name = 'paginas/form.html'
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
class PersonagemCreate(CreateView):
    model = Personagem 
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia', 'user']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}
    
class PersonagemUpdate(UpdateView):
    model = Personagem
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia', 'user']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class ConversaCreate(CreateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}

class MensagemCreate(CreateView):
    model = Mensagem
    fields = ['enviada_por', 'enviada_em', 'origem', 'conteudo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {}