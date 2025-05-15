from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome = models.CharField(max_length=100)
    data_nasc = models.DateField
    email = models.EmailField
    nickname = models.CharField(max_length=100)
    id = models.CharField(max_length=16)
    conversa = models.ForeignKey(Conve)
    
    

class Universo(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(1500, verbose_name="Descrição")
    
class Personagem(models.Model):
    nome = models.TextField(100)
    habilidades = models.TextField(1000)
    caracteristicas = models.TextField(1000, verbose_name="Características)
    origem = models.TextField(1500)
    user = models.ForeignKey(PerfilUsuario, on_delete= Protect)
    
class Conversa(models.Model):
    usuarios = models.ForeignKey(Usuario, on_delete=Protect)
    u 