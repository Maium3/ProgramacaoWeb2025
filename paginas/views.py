from django.views.generic import TemplateView, ListView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate, Favoritos


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm
from django .shortcuts import get_object_or_404
from django.utils import timezone


# Crie a view no final do arquivo ou em outro local que faça sentido
class CadastroUsuarioView(CreateView):
    # Não tem o fields, pois ele é definido no forms.py
    form_class = UsuarioCadastroForm
    # Pode utilizar o seu form padrão
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_usuarios')
    success_message = "Usuário %(username)s cadastrado com sucesso"
    extra_context = {
        'titulo': 'Registro de usuários',
        'botao': 'Registrar',
    }


    def form_valid(self, form):
        # pegar nome e data_nasc do form
        nome = form.cleaned_data.get('nome')
        data_nasc = form.cleaned_data.get('data_nasc')

        # Faz o comportamento padrão do form_valid
        url = super().form_valid(form)
        # Busca ou cria um grupo com esse nome
        grupo, criado = Group.objects.get_or_create(name='Usuários Comuns')
        # Acessa o objeto criado e adiciona o usuário no grupo acima
        self.object.groups.add(grupo)

        # Gera um código_id será o primeiro nome sem espaço em minúsculo + # + id do usário sempre formatado com pelo menos 4 dígitos
        codigo_id = f"{nome.split()[0].lower()}#{self.object.id:04d}"
        # Exemplo: João Silva -> joão#0001

        # Cria o objeto Usuario com os dados adicionais
        Usuario.objects.create(
            usuario=self.object,
            nome=nome,
            data_nasc=data_nasc,
            codigo_id=codigo_id  # Exemplo simples de código ID
        )
        # Retorna a URL de sucesso
        return url



class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView(TemplateView):
    template_name = 'paginas/sobre.html'
    
  
class UsuarioCreate(SuccessMessageMixin, CreateView):
    model = Usuario
    fields = ['nome', 'data_nasc']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_usuarios')
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
    success_url = reverse_lazy('listar_personagens')
    success_message = "Personagem criado com sucesso"
    extra_context = {
        'titulo': 'Criar Personagem',
        'botao': 'Criar'
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        url = super().form_valid(form)
        self.success_message = f"O Personagem {form.instance.nome} foi criado com sucesso"
        return url
    
class ConversaCreate(LoginRequiredMixin, CreateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_conversas')
    extra_context = {
        'titulo': "iniciar nova conversa",
        'botao': "Iniciar"

    }

    def form_valid(self, form):
        form.instance.usuarios = self.request.user
        url = super().form_valid(form)
        self.success_message = "A conversa foi iniciada com sucesso"
        return url

class MensagemCreate(LoginRequiredMixin, CreateView):
    model = Mensagem
    fields = ['enviada_por', 'enviada_em', 'conteudo', 'conversa_origem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "Enviar mensagem",
        'botao': "Enviar"
    }

    def form_valid(self, form):
        form.instance.enviada_por = Personagem.objects.get(user=self.request.user)
        form.instance.enviada_em = form.instance.enviada_em or timezone.now()
        url = super().form_valid(form)
        self.success_message = "Mensagem enviada com sucesso"
        return url

class CombateCreate(LoginRequiredMixin, CreateView):
    model = Combate
    fields = ['conversa', 'mensagem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_Combates')
    success_message = "Combate iniciado com sucesso"
    extra_context = {
        'titulo': "Iniciar novo combate",
        'botao': "Iniciar"
    }

class FavoritoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Favoritos
    fields = ['user','amigo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_contatos')
    success_message = "Usuário adcionado com sucesso"
    extra_context = {
        'titulo': 'Salvar novo contato',
        'botao': 'Salvar'   
    }

    def form_valid(self, form):
        form.instance.proprietario = self.request.user
        url = super().form_valid(form)
        self.success_message = "Contato adicionado com sucesso"
        return url



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

    #alterar o metodo que busca o objeto pelo id(get_object)
    def get_object(self, queryset=None):
        return get_object_or_404(Usuario, pk=self.kwargs['pk'], )
    
    
    
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
    success_url = reverse_lazy('listar_personagens')
    
    success_message = "O Personagem %(nome)% foi atualizado com sucesso"
    extra_context = {  
        'titulo': 'Alterar Personagem',
        'botao': 'Alterar'
    }

class ConversaUpdate(LoginRequiredMixin, UpdateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "Modificar conversa",
        'botao': "Modificar"
    }

    
class MensagemUpdate(LoginRequiredMixin, UpdateView):
    model = Mensagem
    fields = ['enviada_por', 'enviada_em', 'conteudo', 'conversa_origem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_mensagens')
    success_message = "Mensagem atualizada com sucesso"
    extra_context = {
        'titulo': "Carregar mensagem",
        'botao': "Carregar"
    }


class UsuarioDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário foi deletado com sucesso"
    extra_context = {
        'titulo': 'Deletar Usuário',
        'botao': 'Deletar'
    }

class PersonagemDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Personagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_personagens')
    success_message = "O Personagem %(nome)% foi deletado com sucesso"
    extra_context = {  
        'titulo': 'Deletar Personagem',
        'botao': 'Deletar'
    }


class ConversaDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Conversa
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Conversa deletada com sucesso"
    extra_context = {
        'titulo': 'Excluir conversa',
        'botao': 'Excluir'
    }


class MensagemDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Mensagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_mensagens')
    success_message = "Mensagem deletada com sucesso"
    extra_context = {
        'titulo': 'Excluir mensagem',
        'botao': 'Excluir'
    }

class FavoritoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Favoritos
    fields = ['amigo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_contatos')
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

class MeusPersonagens(PersonagemList):
    def get_queryset(self):
        qs = Personagem.objects.filter(user=self.request.user)
        return qs


class ConversaList(LoginRequiredMixin, ListView):
    model= Conversa
    template_name = "paginas/conversa.html" 

class MensagemList(LoginRequiredMixin, ListView):
    model= Mensagem
    template_name = "paginas/mensagem.html"


class CombateList(ListView):
    model= Combate
    template_name = "paginas/usuario.html" 

class FavoritoList(ListView):
    model= Favoritos
    template_name= "paginas/favoritos.html"

