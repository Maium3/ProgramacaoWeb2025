from django.contrib import admin
from .models import Usuario, Universo, Personagem, Conversa, Mensagem, Combate, Favoritos

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Universo)
admin.site.register(Personagem)
admin.site.register(Conversa)
admin.site.register(Mensagem)
admin.site.register(Combate)
admin.site.register(Favoritos)