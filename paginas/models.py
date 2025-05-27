from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome = models.CharField(max_length=100)
    data_nasc = models.DateField
    email = models.EmailField
    nickname = models.CharField(max_length=100)
    id = models.CharField(max_length=16) 

    def __str__(self):
        return self.usuario, self.nome, self.data_nasc, self.email, self.nickname, self.id

class Universo(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(1500, verbose_name="Descrição")
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.nome, self.descricao, self.data_criacao, self.ultima_atualizacao
    
class Personagem(models.Model):
    nome = models.TextField(100)
    habilidades = models.TextField(1000)
    caracteristicas = models.TextField(1000, verbose_name="Características", null=True) 
    historia = models.TextField(1500, null=True)
    user = models.ForeignKey(User, on_delete= models.PROTECT)

    def __str__(self):
        return  self.nome, self.habilidades, self.caracteristicas, self.historia, self.user.nickname, self.user.id
    
class Conversa(models.Model):
    usuarios = models.ForeignKey(User, on_delete= models.PROTECT)
    universo = models.ForeignKey(Universo, on_delete= models.PROTECT)

    def __str__(self):
        return  self.usuarios.nickname, self.universo.nome

class Mensagem(models.Model):
    enviada_por = models.ForeignKey(Personagem, on_delete = models.PROTECT)
    enviada_em = models.DateTimeField(auto_now_add=True)
    conversa_origem = models.ForeignKey(Conversa, on_delete=models.CASCADE)
    conteudo = models.TextField(1500)

    def __str__(self):
        return  self.enviada_por, self.enviada_em, self.conteudo

class Combate(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete = models.CASCADE)
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE)

    def __str__(self):
        return  self.conversa, self.mensagem
        