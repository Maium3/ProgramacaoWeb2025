from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="usuário", related_name="perfil")
    nome = models.CharField(max_length=100)
    data_nasc = models.DateField(verbose_name="data de nascimento")
    codigo_id = models.CharField(max_length=16, verbose_name="ID", unique=True) 

    def __str__(self):
        return f"{self.usuario} ({self.codigo_id})"
    

class Universo(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(verbose_name="descrição")
    criado_por = models.ForeignKey(User, on_delete= models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="data de criação")
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="última atualização")

    def __str__(self):
        return  f"{self.nome} - Criado por {self.criado_por}"
    
    
class Personagem(models.Model):
    nome = models.CharField(max_length=100)
    habilidades = models.TextField()
    caracteristicas = models.TextField(verbose_name="características", null=True, blank=True) 
    historia = models.TextField(verbose_name="história", null=True, blank=True)
    universo_origem = models.ForeignKey(Universo, on_delete=models.PROTECT)
    

    def __str__(self):
        return  f"{self.nome} ({self.criado_por})"
    
    
class Conversa(models.Model):
    titulo = models.CharField(max_length=255, verbose_name="Título")
    personagens = models.ManyToManyField(Personagem, verbose_name="Personagens")
    universo = models.ForeignKey(Universo, on_delete=models.PROTECT)
    
    def __str__(self):
        return  f"{self.titulo} ({self.universo})"
    

class Mensagem(models.Model):
    enviada_por = models.ForeignKey(Personagem, on_delete = models.PROTECT)
    enviada_em = models.DateTimeField(auto_now_add=True)
    conversa_origem = models.ForeignKey(Conversa, on_delete=models.CASCADE)
    conteudo = models.TextField(verbose_name="Conteúdo")

    def __str__(self):
        return  f"{self.enviada_por} disse: {self.conteudo}"


class Combate(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete = models.CASCADE)
    mensagem = models.ForeignKey(Mensagem, on_delete=models.CASCADE)
    # criar o atributo mestre_da_mesa que deverá inserir um usuário mestre
    ganhador = models.ForeignKey(Personagem, on_delete=models.CASCADE, related_name='ganhador')
    perdedor = models.ForeignKey(Personagem, on_delete=models.CASCADE, related_name='perdedor')

    def __str__(self):
        return  f"Combate em {self.conversa}: Ganhador {self.ganhador} - Perdedor {self.perdedor}"
        
class Favoritos(models.Model):
    proprietario = models.ForeignKey(User, on_delete= models.CASCADE, related_name="proprietario")
    amigo = models.ForeignKey(User, on_delete= models.CASCADE, related_name="amigo")

    def __str__(self):
        return  f"{self.proprietario} é amigo de {self.amigo}"