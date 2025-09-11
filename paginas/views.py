from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate, Favoritos


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm
from django .shortcuts import get_object_or_404
from django.utils import timezone



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
        grupo1, criado = Group.objects.get_or_create(name='Player ')
        grupo2, criado = Group.objects.get_or_create(name='Mestre')
        grupo3, criado = Group.objects.get_or_create(name='Administrador')
        # Acessa o objeto grupo1 e grupo2 criados e permite o usuário decidir em qual grupo sera adcionado

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


# DetailView para exibir conversa e suas mensagens
class ConversaDetailView(DetailView):
    model = Conversa
    template_name = 'paginas/detalhe_conversa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca todas as mensagens relacionadas a esta conversa
        context['mensagens'] = self.object.mensagem_set.all()
        return context



class Inicio(TemplateView):
    template_name = "paginas/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

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

    # def form_valid(self, form):
    #     form.instance.usuarios = self.request.user
    #     url = super().form_valid(form)
    #     self.success_message = "A conversa foi iniciada com sucesso"
    #     return url

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

class CombateCreate(GroupRequiredMixin, CreateView):
    group_required= ["Mestre"]
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
    fields = ['nome', 'data_nasc', 'username', 'email']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário foi atualizado com sucesso"
    extra_context = {
        'titulo': 'Atualuzar meus dados',
        'botao': 'Confirmar'   
    }

    #alterar o metodo que busca o objeto pelo id(get_object) para que só o proprio usuario possa alterar seus dados
    def get_object(self, queryset=None):
        return get_object_or_404(Usuario, pk=self.kwargs['pk'], usuario=self.request.user)
    
    
    
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

    #alterar o metodo que busca o objeto pelo id(get_object) para que só o proprio usuario possa alterar seus dados
    def get_object(self, queryset=None):
        return get_object_or_404(Universo, pk=self.kwargs['pk'], usuario=self.request.user)
    

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

    def get_object(self, queryset=None):
        return get_object_or_404(Personagem, pk=self.kwargs['pk'], user=self.request.user)

class ConversaUpdate(LoginRequiredMixin, UpdateView):
    model = Conversa
    fields = ['usuarios', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "Modificar conversa",
        'botao': "Modificar"
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Conversa, pk=self.kwargs['pk'], usuarios=self.request.user)

    
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

    def get_object(self, queryset=None):
        return get_object_or_404(Mensagem, pk=self.kwargs['pk'], enviada_por__user=self.request.user)


class UsuarioDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Usuário foi deletado com sucesso"
    extra_context = {
        'titulo': 'Deletar Usuário',
        'botao': 'Deletar'
    }

    #alterar o metodo que busca o objeto pelo id(get_object) para que só o proprio usuario possa apagar seus dados
    def get_object(self, queryset=None):
        return get_object_or_404(Usuario, pk=self.kwargs['pk'], usuario=self.request.user)


class PersonagemDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Personagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_personagens')
    success_message = "O Personagem %(nome)% foi deletado com sucesso"
    extra_context = {  
        'titulo': 'Deletar Personagem',
        'botao': 'Deletar'
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Personagem, pk=self.kwargs['pk'], user=self.request.user)


class ConversaDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Conversa
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    success_message = "Conversa deletada com sucesso"
    extra_context = {
        'titulo': 'Excluir conversa',
        'botao': 'Excluir'
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Conversa, pk=self.kwargs['pk'], usuarios=self.request.user)


class MensagemDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Mensagem
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_mensagens')
    success_message = "Mensagem deletada com sucesso"
    extra_context = {
        'titulo': 'Excluir mensagem',
        'botao': 'Excluir'
    }

    def get_object(self, queryset=None):
        return get_object_or_404(Mensagem, pk=self.kwargs['pk'], enviada_por__user=self.request.user)

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

    def get_object(self, queryset=None):    
        return get_object_or_404(Favoritos, pk=self.kwargs['pk'], proprietario=self.request.user)
 

class UsuarioList(LoginRequiredMixin, ListView):
    model= Usuario
    template_name = "paginas/listas/usuario.html"

    # filtrar para mostrar apenas os dados do proprio usuario, exceto para o superuser
    # se for superuser, mostrar todos os usuarios
    #deve mostrar também todos os dados dos usuarios, como nome, data_nasc, email, username, id e senha(password), para o superuser
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        else:
            return Usuario.objects.filter(usuario=self.request.user)
             


class UniversoList(ListView):
    model= Universo
    template_name = "paginas/listas/universo.html"
    


class PersonagemList(ListView):
    model= Personagem
    template_name = "paginas/listas/personagem.html"

class MeusPersonagens(PersonagemList):
    def get_queryset(self):
        qs = Personagem.objects.filter(user=self.request.user)
        return qs


class ConversaList(LoginRequiredMixin, ListView):
    model= Conversa
    template_name = "paginas/listas/conversa.html" 
    def get_queryset(self):
        qs = Conversa.objects.filter(usuarios=self.request.user)
        return qs

class MensagemList(LoginRequiredMixin, ListView):
    model= Mensagem
    template_name = "paginas/listas/mensagem.html"
    #filtrar para mostrar apenas as mensagens enviadas pelo proprio usuario ou para ele
    def get_queryset(self):
        qs = Mensagem.objects.filter(enviada_por__user=self.request.user)
        return qs 


class CombateList(ListView):
    model= Combate
    template_name = "paginas/listas/usuario.html" 

class FavoritoList(ListView):
    model= Favoritos
    template_name= "paginas/listas/favoritos.html"
    def get_queryset(self):
        qs = Favoritos.objects.filter(proprietario=self.request.user)
        return qs

