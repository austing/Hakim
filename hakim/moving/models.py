# -*- coding: utf-8 -*-

from django.db import models
from django_extensions.db.fields import AutoSlugField
from decimal import Decimal

# Create your models here.
class Chambre(models.Model):
    nom = models.CharField(max_length=200)
    slug = AutoSlugField('slug', max_length=50, unique=True, populate_from=('nom',))

    def __unicode__(self):
        return self.nom

class Meuble(models.Model):
    nom = models.CharField(max_length=200)
    nom_pluriel = models.CharField(max_length=200)
    chambre = models.ForeignKey(Chambre)
    slug = AutoSlugField('slug', max_length=50, unique=True, populate_from=('nom',))
    volume = models.DecimalField(decimal_places=2,max_digits=9)
    
    def __unicode__(self):
        return self.nom

class MeubleQuantite(models.Model):
    meuble = models.ForeignKey(Meuble)
    quantite = models.PositiveIntegerField()

class CommandeParticulier(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200,verbose_name="Prénom")
    CIVILITE_CHOICES = (("Blanc","Civilité"),("M.","M."),("Mme","Mme"),)
    civilite = models.CharField(choices=CIVILITE_CHOICES, max_length=5, null=False, blank=False, default="Blanc")
    mail = models.EmailField(verbose_name="Email")
    phone_domicile = models.IntegerField(verbose_name="Téléphone domicile",blank=True, null=True)
    phone_cell = models.IntegerField(verbose_name="Téléphone mobile",blank=True, null=True)
    origine_ville = models.CharField(max_length=200, verbose_name="Ville de départ")
    origine_addresse = models.CharField(blank=True,max_length=200)
    origine_code = models.CharField(max_length=200, verbose_name="Code postal", blank=True)
    origine_etages = models.IntegerField(default=0,verbose_name="Etages")
    ascenseur_origine = models.BooleanField(verbose_name="Ascenseur?")
    destination_ville = models.CharField(max_length=200, verbose_name="Ville d'arrivée")
    destination_addresse = models.CharField(blank=True,max_length=200)
    destination_code = models.CharField(max_length=200, verbose_name="Code postal", blank=True)
    destination_etages = models.IntegerField(default=0,verbose_name="Etages")
    ascenseur_destination = models.BooleanField(verbose_name="Ascenseur?")
    date_chargement = models.DateField(verbose_name="Date chargement")
    date_dechargement = models.DateField(verbose_name="Date déchargement")
    meubles = models.ManyToManyField(MeubleQuantite)
    volume = models.DecimalField(decimal_places=2, max_digits=9, verbose_name="Volume (m3)")
    DEVIS = 'DV'
    FINALISE = 'FN'
    ETAT_CHOICES = (
        (DEVIS, 'Demande de devis'),
        (FINALISE, 'Finalisé')
    )
    etat_de_commande = models.CharField(max_length=2,
                choices=ETAT_CHOICES, default=DEVIS)

    def calculer_volume(self):
        # if the user has set volume manually, this should never be called to overwrite existing value!.
        volume = Decimal(0)
        for meubles_quantite in self.meubles.all():
            volume += meubles_quantite.quantite*meubles_quantite.meuble.volume
        return volume

    def save(self, *args, **kwargs):
        if not self.volume:
            if not self.pk:
                super(CommandeParticulier,self).save(*args,**kwargs)
                self.volume = self.calculer_volume()
                self.save()
            else:
                self.volume = self.calculer_volume()     
        return super(CommandeParticulier,self).save(*args,**kwargs)

class CommandeProfessionnel(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200,verbose_name="Prénom")
    CIVILITE_CHOICES = (("Blanc","Civilité"),("M.","M."),("Mme","Mme"),)
    civilite = models.CharField(choices=CIVILITE_CHOICES, max_length=5, null=False, blank=False, default="Blanc")
    mail = models.EmailField(verbose_name="Email")
    phone_domicile = models.IntegerField(verbose_name="Téléphone domicile",blank=True, null=True)
    phone_cell = models.IntegerField(verbose_name="Téléphone mobile",blank=True, null=True)
    origine_ville = models.CharField(max_length=200, verbose_name="Ville de départ")
    origine_addresse = models.CharField(blank=True,max_length=200)
    origine_code = models.CharField(max_length=200, verbose_name="Code postal", blank=True)
    origine_etages = models.IntegerField(default=0,verbose_name="Etages")
    ascenseur_origine = models.BooleanField(verbose_name="Ascenseur?")
    destination_ville = models.CharField(max_length=200, verbose_name="Ville d'arrivée")
    destination_addresse = models.CharField(blank=True,max_length=200)
    destination_code = models.CharField(max_length=200, verbose_name="Code postal", blank=True)
    destination_etages = models.IntegerField(default=0,verbose_name="Etages")
    ascenseur_destination = models.BooleanField(verbose_name="Ascenseur?")
    date_chargement = models.DateField(verbose_name="Date chargement")
    date_dechargement = models.DateField(verbose_name="Date déchargement")
    meubles = models.ManyToManyField(MeubleQuantite)
    volume = models.DecimalField(decimal_places=2, max_digits=9, verbose_name="Volume (m3)")
    DEVIS = 'DV'
    FINALISE = 'FN'
    ETAT_CHOICES = (
        (DEVIS, 'Demande de devis'),
        (FINALISE, 'Finalisé')
    )
    etat_de_commande = models.CharField(max_length=2,
                choices=ETAT_CHOICES, default=DEVIS)
'''
    def calculer_volume(self):
        # if the user has set volume manually, this should never be called to overwrite existing value!.
        volume = Decimal(0)
        for meubles_quantite in self.meubles.all():
            volume += meubles_quantite.quantite*meubles_quantite.meuble.volume
        return volume

    def save(self, *args, **kwargs):
        if not self.volume:
            if not self.pk:
                super(CommandeParticulier,self).save(*args,**kwargs)
                self.volume = self.calculer_volume()
                self.save()
            else:
                self.volume = self.calculer_volume()     
        return super(CommandeParticulier,self).save(*args,**kwargs)
'''