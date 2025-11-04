from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import  CreateView, UpdateView, DeleteView
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate, Favoritos


from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.views import View
from django.utils import timezone
from django.http import Http404



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
class ConversaDetailView(LoginRequiredMixin, DetailView):
    model = Conversa
    template_name = 'paginas/detalhe_conversa.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca todas as mensagens relacionadas a esta conversa
        context['mensagens'] = self.object.mensagem_set.all().order_by('enviada_em')
        # Filtrar DENTRO DOS PERSONAGENS desta conversa, aqueles que foram criados pelo usuário logado
        # self.object é a conversa atual
        # então self.object.personagens é a lista de personagens dessa conversa
        # Assim, aplico um filtro para pegar apenas os personagens cujo criado_por é o usuário logado
        context['meus_personagens'] = self.object.personagens.filter(criado_por=self.request.user)
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

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)
    
class PersonagemCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Personagem 
    fields = ['universo', 'nome', 'habilidades', 'caracteristicas', 'historia' ]
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_personagens')
    success_message = "Personagem criado com sucesso"
    extra_context = {
        'titulo': 'Criar Personagem',
        'botao': 'Criar'
    }

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        url = super().form_valid(form)
        self.success_message = f"O Personagem {form.instance.nome} foi criado com sucesso"
        return url
    
class ConversaCreate(LoginRequiredMixin, CreateView):
    model = Conversa
    fields = ['titulo', 'universo']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_conversas')
    extra_context = {
        'titulo': "iniciar nova conversa",
        'botao': "Iniciar"
    }

    # Definir os personagens disponívels somente aqueles que fazem parte do universo desta conversa
    # def get_form(self, *args, **kwargs):
    #     form = super().get_form(*args, **kwargs)
    #     universo_id = self.request.GET.get('universo_id')
    #     if universo_id:
    #         form.fields['universo'].initial = universo_id
    #         form.fields['universo'].widget.attrs['readonly'] = True
    #         form.fields['personagens'].queryset = Personagem.objects.filter(universo__id=universo_id)
    #     else:
    #         form.fields['personagens'].queryset = Personagem.objects.none()
    #     return form


    # def form_valid(self, form):
    #     form.instance.usuarios = self.request.user
    #     url = super().form_valid(form)
    #     self.success_message = "A conversa foi iniciada com sucesso"
    #     return url

class MensagemCreate(LoginRequiredMixin, CreateView):
    model = Mensagem
    fields = ['conversa_origem', 'conteudo', 'enviada_por']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "Enviar mensagem",
        'botao': "Enviar"
    }

    def get_form(self, *args, **kwargs):
        # Listar apenas os personagens criados pelo usuário logado
        form = super().get_form(*args, **kwargs)
        form.fields['enviada_por'].queryset = Personagem.objects.filter(criado_por=self.request.user)
        # Se recebe um paramétro 'conversa_id' na URL, preenche o campo conversa_origem com essa conversa e torna o campo readonly
        conversa_id = self.request.GET.get('conversa_id')
        if conversa_id:
            form.fields['conversa_origem'].initial = conversa_id
            form.fields['conversa_origem'].widget.attrs['readonly'] = True
        return form
    
    # Ao cadastrar a mensagem, redirecione para a url do DetailView de conversa
    def get_success_url(self):
        return reverse_lazy('detalhe_conversa', kwargs={'pk': self.object.conversa_origem.pk})

    


class CombateCreate(GroupRequiredMixin, SuccessMessageMixin, CreateView):
    group_required= ["Mestre"]
    model = Combate
    fields = ['conversa', 'ganhador', 'perdedor']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_Combates')
    success_message = "Combate iniciado com sucesso"
    extra_context = {
        'titulo': "Iniciar novo combate",
        'botao': "Iniciar"
    }

    def form_valid(self, form):
        form.instance.mestre_da_mesa = self.request.user
        return super().form_valid(form)

class FavoritoCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Favoritos
    fields = ['amigo']
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
        'titulo': 'Atualizar meus dados',
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

    def get_object(self, queryset=None):
        obj = get_object_or_404(Universo, pk=self.kwargs['pk'])
        if obj.criado_por != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para editar este universo.")
        return obj
    

class PersonagemUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Personagem 
    fields = ['nome', 'habilidades', 'caracteristicas', 'historia']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_personagens')
    
    success_message = "O Personagem %(nome)s foi atualizado com sucesso"
    extra_context = {  
        'titulo': 'Alterar Personagem',
        'botao': 'Alterar'
    }

    def get_object(self, queryset=None):
        obj = get_object_or_404(Personagem, pk=self.kwargs['pk'])
        if obj.criado_por != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para editar este personagem.")
        return obj

class ConversaUpdate(LoginRequiredMixin, UpdateView):
    model = Conversa
    fields = ['personagens']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('Inicio')
    extra_context = {
        'titulo': "Modificar conversa",
        'botao': "Modificar"
    }

    # Filtrar no form somente os personagens que fazem parte do mesmo universo
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        universo = self.get_object().universo
        form.fields['personagens'].queryset = Personagem.objects.filter(universo=universo)
        return form

    def get_object(self, queryset=None):
        obj = get_object_or_404(Conversa, pk=self.kwargs['pk'])
        if not obj.personagens.filter(criado_por=self.request.user).exists() and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para editar esta conversa.")
        return obj

    
class MensagemUpdate(LoginRequiredMixin, UpdateView):
    model = Mensagem
    fields = ['enviada_por', 'conteudo', 'conversa_origem']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_mensagens')
    success_message = "Mensagem atualizada com sucesso"
    extra_context = {
        'titulo': "Carregar mensagem",
        'botao': "Carregar"
    }

    def get_object(self, queryset=None):
        obj = get_object_or_404(Mensagem, pk=self.kwargs['pk'])
        if obj.enviada_por.criado_por != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para editar esta mensagem.")
        return obj


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


class UniversoDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Universo
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_Universos')
    success_message = "Universo deletado com sucesso"
    extra_context = {
        'titulo': 'Excluir Universo',
        'botao': 'Excluir'
    }

    def get_object(self, queryset=None):
        obj = get_object_or_404(Universo, pk=self.kwargs['pk'])
        if obj.criado_por != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para excluir este universo.")
        return obj


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
        obj = get_object_or_404(Personagem, pk=self.kwargs['pk'])
        if obj.criado_por != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para excluir este personagem.")
        return obj


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
        obj = get_object_or_404(Conversa, pk=self.kwargs['pk'])
        if not obj.personagens.filter(criado_por=self.request.user).exists() and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para excluir esta conversa.")
        return obj


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
        obj = get_object_or_404(Mensagem, pk=self.kwargs['pk'])
        if obj.enviada_por.criado_por != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para excluir esta mensagem.")
        return obj

class FavoritoDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Favoritos
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar_contatos')
    success_message = "Usuário excluido com sucesso"
    extra_context = {
        'titulo': 'Excluir contato',
        'botao': 'Excluir'   
    }

    def get_object(self, queryset=None):
        obj = get_object_or_404(Favoritos, pk=self.kwargs['pk'])
        if obj.proprietario != self.request.user and not self.request.user.groups.filter(name='Administrador').exists():
            raise Http404("Você não tem permissão para excluir este favorito.")
        return obj
 

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
            

class UniversoList(LoginRequiredMixin, ListView):
    model= Universo
    template_name = "paginas/listas/universo.html"
    

class PersonagemList(LoginRequiredMixin, ListView):
    model= Personagem
    template_name = "paginas/listas/personagem.html"


class MeusPersonagens(PersonagemList):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(criado_por=self.request.user)
        return qs


class ConversaList(LoginRequiredMixin, ListView):
    model= Conversa
    template_name = "paginas/listas/conversa.html" 

    # Se receber um parâmetro 'universo_id' na URL, filtra as conversas por esse universo
    def get_queryset(self):
        qs = super().get_queryset()
        # Se recebe o universo_id do kwargs
        universo_id = self.kwargs.get('universo_id')
        if universo_id:
            qs = qs.filter(universo__id=universo_id)
        return qs


class MinhasConversasList(LoginRequiredMixin, ListView):
    model= Conversa
    template_name = "paginas/listas/conversa.html"

    def get_queryset(self):
        qs = super().get_queryset()
        # Lista todas as conversas de um universo que tenham personagens criados pelo usuário logado
        qs = qs.filter(personagens__criado_por=self.request.user).distinct()
        return qs
    

class MensagemList(LoginRequiredMixin, ListView):
    model= Mensagem
    template_name = "paginas/listas/mensagem.html"
    # Se recebe o id de uma conversa, filtra as mensagens dessa conversa
    def get_queryset(self):
        qs = super().get_queryset()
        conversa_id = self.request.GET.get('conversa_id')
        if conversa_id:
            qs = qs.filter(conversa_origem__id=conversa_id)
        return qs 
    

class MinhasMensagensList(LoginRequiredMixin, ListView):
    model= Mensagem
    template_name = "paginas/listas/mensagem.html"

    # Filtra as mensagens de conversas que tem somente meu personagem
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(enviada_por__criado_por=self.request.user)
        return qs


class CombateList(ListView):
    model= Combate
    template_name = "paginas/listas/combate.html" 


class FavoritoList(ListView):
    model= Favoritos
    template_name= "paginas/listas/favoritos.html"
    # Filtra favoritos do usuário logado
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(proprietario=self.request.user)
        return qs
