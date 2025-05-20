from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome = models.CharField(max_length=100)
    data_nasc = models.DateField
    email = models.EmailField
    nickname = models.CharField(max_length=100)
    id = models.CharField(max_length=16) 
    

class Universo(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(1500, verbose_name="Descrição")
    
class Personagem(models.Model):
    nome = models.TextField(100)
    habilidades = models.TextField(1000)
    caracteristicas = models.TextField(1000, verbose_name="Características")
    historia = models.TextField(1500)
    user = models.ForeignKey(User, on_delete= models.PROTECT)
    
class Conversa(models.Model):
    usuarios = models.ForeignKey(User, on_delete= models.PROTECT)
    universo = models.ForeignKey(Universo, on_delete= models.PROTECT)


class Mensagem(models.Model):
    enviada_por = models.ForeignKey(Personagem, on_delete = models.PROTECT)
    enviada_em = models.DateTimeField
    origem = models.ForeignKey(Conversa, on_delete=models.CASCADE)
    conteudo = models.TextField(1500)

class Combate(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete = models.CASCADE)
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE)
        