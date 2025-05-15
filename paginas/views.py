from django.views.generic import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class Inicio(TemplateView):
    template_name = "paginas/login.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'
    
  
class UsuarioCreate(CreateView):
    model = Usuario
    template_name = 'paginas/form.html'
    fields = ['nome', 'data_nasc', 'email', 'nickname', 'id']
    success_url = reverse_lazy('pagina/index.html')
    extra_context = {}
    
class UsuarioUpdate(UpdateView):
     model = Usuario
     template_name = 'paginas/form.html'
     fields = ['nome', 'data_nasc', 'email', 'nickname', 'id']
     success_url = reverse_lazy('pagina/index.html')
     extra_context = {}
     
class UniversoCreate(CreateView):
    model = Universo 
    template_name = 'paginas/form.html'
    fields = ['nome','Descrição']
    success_url = reverse_lazy('pagina/index.html')
    extra_context = {}
    
    
class UniversoUpdate(UpdateView):
    model = Universo
    template_name = 'paginas/form.html'
    fields = ['nome', 'Descrição']
    success_url = reverse_lazy('pagina/index.html')
    extra_context = {}
    
class PersonagemCreate(CreateView):
    model = Personagem 
    template_name = 'paginas/form.html'
    fields = ['nome', 'habilidades', 'Características', 'origem', 'User']
    success_url = reverse_lazy('pagina/index.html')
    extra_context = {}
    
class PersonagemUpdate(UpdateView):
    model = Personagem
    template_name = 'paginas/form.html'
    fields = ['nome', 'habilidades', 'Características', 'origem', 'User']
    success_url = reverse_lazy('pagina/index.html')
    extra_context = {}

