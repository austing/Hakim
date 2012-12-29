from django.contrib import admin

from moving.models import CommandeParticulier, MeubleQuantite, Meuble, Chambre

admin.site.register(CommandeParticulier)
admin.site.register(MeubleQuantite)
admin.site.register(Meuble)
admin.site.register(Chambre)