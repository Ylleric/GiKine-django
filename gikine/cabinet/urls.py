from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='cabinet-home'),
    path('kinesitherapeutes', views.kinesitherapeutes, name='cabinet-kinesitherapeutes'),
    path('kinesitherapeutes/<id>', views.kinesitherapeute_info, name='cabinet-kinesitherapeute-info'),
    path('patients', views.patients, name='cabinet-patients'),
    path('patients/<id>', views.patient_info, name='cabinet-patient-info'),
    path('medecins', views.medecins, name='cabinet-medecins'),
    path('medecins/<id>', views.medecin_info, name='cabinet-medecin-info'),
    path('ordonnance/<id>', views.ordonnance_info, name='cabinet-ordonnance-info'),
    path('factures', views.factures, name='cabinet-factures'),
    path('factures/<annee>', views.factures_annee, name='cabinet-factures-annee'),
    path('factures/<annee>/<mois>', views.factures_mois, name='cabinet-factures-mois'),
    path('facture/<id>', views.facture_info, name='cabinet-facture-info'),
    path('chiffre_affaire', views.chiffre_affaire, name='cabinet-chiffre_affaire'),
]