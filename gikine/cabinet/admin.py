from django.contrib import admin
from .models import Facture, Kinesitherapeute, Medecin, Ordonnance, Patient, Prestation, TypePatient, Seance


class FactureAdmin(admin.ModelAdmin):
    list_display   = ('numero', 'patient', 'tiers', 'montant', 'paye')
    list_filter    = ('paye', )
    search_fields  = ('numero', 'patient', 'tiers')
    ordering       = ('-numero', )


class KinesitherapeuteAdmin(admin.ModelAdmin):
    list_display   = ('initiale', 'nom', 'numero')
    search_fields  = ('initiale', 'nom', )


class MedecinAdmin(admin.ModelAdmin):
    list_display   = ('matricule', 'rue', 'nom', 'specialite', 'actif')
    search_fields  = ('nom','matricule')


class OrdonnanceAdmin(admin.ModelAdmin):
    list_display   = ('numero', 'statut', 'patient', 'medecin', 'taux', 'prestations_max')
    list_filter    = ('statut', 'taux', 'prestations_max')
    search_fields  = ('numero',)
    ordering       = ('-numero', )


class PatientAdmin(admin.ModelAdmin):
    list_display   = ('nom', 'rue', 'code_postal', 'ville', 'matricule', 'typePatient')
    list_filter    = ('sexe',  )
    search_fields  = ('nom', 'sexe', )


class PrestationAdmin(admin.ModelAdmin):
    list_display   = ('numero', 'code_acte', 'date_prestation', 'patient', 'prix_acte', 'date_periode')
    list_filter    = ('patient', )
    search_fields  = ('numero', )
    ordering       = ('-numero', )

class SeanceAdmin(admin.ModelAdmin):
    list_display   = ('numero', 'patient', 'ordonnance', 'effectuee', 'date_seance', 'date_facture')
    list_filter    = ('effectuee', 'patient', )
    search_fields  = ('numero', )
    ordering       = ('-numero', )

class TypePatientAdmin(admin.ModelAdmin):
    list_display   = ('nom', )
    search_fields  = ('nom', )


admin.site.register(Facture,FactureAdmin)
admin.site.register(Kinesitherapeute, KinesitherapeuteAdmin)
admin.site.register(Medecin,MedecinAdmin)
admin.site.register(Ordonnance,OrdonnanceAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(Seance, SeanceAdmin)
admin.site.register(TypePatient, TypePatientAdmin)