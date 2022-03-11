from django.conf import settings
from django.utils.translation import get_language
from django.db.models import aggregates, F
from django.db.models.aggregates import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render, get_object_or_404
from .models import Facture, Medecin, Ordonnance, Patient, Kinesitherapeute, Prestation, Kinesitherapeute, Seance
import calendar
from datetime import datetime, timedelta

def home(request):
    date_fin = datetime.today()
    date_debut = date_fin - timedelta(settings.JOURS_MAX)
    date_expiration = date_fin + timedelta(settings.JOURS_EXPIRATION_MAX)

    liste_prestations = Prestation.objects.filter(date_prestation__range=[date_debut, date_fin]).values('date_prestation').annotate(date_prestation_count=Count('date_prestation')).order_by('-date_prestation')
    listes_ordonnances = Ordonnance.objects.filter(date_fin_validite__range = [date_fin, date_expiration]).annotate(seances=Count('prestation__numero',distinct=True)).annotate(seances_restantes = F('prestations_max') - F('seances')).exclude(seances_restantes=0).order_by('-date_fin_validite')
    liste_factures = Facture.objects.filter(date_creation__range=[date_debut, date_fin] ).values('patient__nom','patient', 'paye').annotate(total_factures=Sum('montant')).order_by('-total_factures')

    context = {
        'nombre_jours_avant_expiration' : settings.JOURS_EXPIRATION_MAX,
        'nombre_jours': settings.JOURS_MAX,
        'liste_prestations': liste_prestations,
        'listes_ordonnances' : listes_ordonnances,
        'liste_factures' : liste_factures
    }
    return render(request, 'cabinet/home.html', context)

def kinesitherapeutes(request):
    kinesitherapeutes = Kinesitherapeute.objects.all()

    context = {
        'kinesitherapeutes' : kinesitherapeutes,
    }
    return render(request, 'cabinet/kinesitherapeutes.html', context)

def kinesitherapeute_info(request, id):
    kinesitherapeute = get_object_or_404(Kinesitherapeute, id=id)
    liste_prestations = Seance.objects.filter(kinesitherapeute = kinesitherapeute.id ).filter(effectuee = True).order_by('-date_seance')

    context = {
        'kinesitherapeute' : kinesitherapeute,
        'liste_prestations' : liste_prestations
    }
    return render(request, 'cabinet/kinesitherapeute_informations.html', context)

def patients(request):
    liste_patients = Patient.objects.all().order_by('nom')

    context = {
        'liste_patients' : liste_patients,
    }
    return render(request, 'cabinet/patients.html', context)

def patient_info(request, id):
    patient = get_object_or_404(Patient, id=id)
    
    liste_ordonnances = Ordonnance.objects.filter(patient = patient).annotate(seances=Count('prestation__numero',distinct=True)).order_by('-date_prescription')
    nombre_ordonnances = liste_ordonnances.aggregate(Count('numero', distinct=True))['numero__count']

    if (patient.id != 1):
        liste_factures = Facture.objects.filter(patient = patient).order_by('-date_creation')
        montant_total_factures = liste_factures.aggregate(Sum('montant'))['montant__sum']
        nombre_factures = liste_factures.aggregate(Count('numero', distinct=True))['numero__count']
        
        liste_factures_cns = Facture.objects.filter(tiers = patient).order_by('-date_creation')
        montant_total_factures_cns = liste_factures_cns.aggregate(Sum('montant'))['montant__sum']
        nombre_factures_cns = liste_factures_cns.aggregate(Count('numero', distinct=True))['numero__count']
    else:
        liste_factures = nombre_factures = montant_total_factures = None
        
        liste_factures_cns = Facture.objects.filter(patient = patient).order_by('-date_creation')
        montant_total_factures_cns = liste_factures_cns.aggregate(Sum('montant'))['montant__sum']
        nombre_factures_cns = liste_factures_cns.aggregate(Count('numero', distinct=True))['numero__count']

    context = {
        'patient' : patient,
        'liste_ordonnances' : liste_ordonnances,
        'nombre_ordonnances' : nombre_ordonnances,
        'liste_factures' : liste_factures,
        'montant_total_factures' : montant_total_factures,
        'nombre_factures' : nombre_factures,
        'liste_factures_cns' : liste_factures_cns,
        'montant_total_factures_cns' : montant_total_factures_cns,
        'nombre_factures_cns' : nombre_factures_cns,
    }
    return render(request, 'cabinet/patient_informations.html', context)

def medecins(request):
    liste_medecins = Medecin.objects.annotate(ordonnance_count=Count('ordonnance')).filter(ordonnance_count__gte=1).order_by('nom')

    context = {
        'liste_medecins': liste_medecins,
    }
    return render(request, 'cabinet/medecins.html', context)

def medecin_info(request, id):
    medecin = get_object_or_404(Medecin, id=id)
    liste_ordonnances_prescrites = Ordonnance.objects.filter(medecin=id)
    
    context = {
        'medecin' : medecin,
        'liste_ordonnances_prescrites': liste_ordonnances_prescrites
    }
    return render(request, 'cabinet/medecin_informations.html', context)

def chiffre_affaire(request):
    labels = {}
    data = {}
    data_count = {}

    today = datetime.today()
    liste_seances = Seance.objects.annotate(year=ExtractYear('date_seance'),month=ExtractMonth('date_seance'),).values('year', 'month').annotate(count_seances=Count('effectuee'))
    liste_factures = Facture.objects.annotate(year=ExtractYear('date_creation'),month=ExtractMonth('date_creation'),).values('year', 'month').annotate(sum_facture=Sum('montant'))
    
    for n in range(settings.ANNEES_MAX):
        liste_data_count = []
        liste_labels = []
        liste_data = []

        total_seances = liste_seances.filter(year = today.year - n).order_by()
        list_chiffre_affaire = liste_factures.filter(year=today.year - n).order_by()
        
        for seance in total_seances:
            liste_data_count.append(seance['count_seances'])

        for chiffre_affaire in list_chiffre_affaire:
            date_temp = datetime.strptime(f"{chiffre_affaire['year']}-{chiffre_affaire['month']}-01", '%Y-%m-%d')
            liste_labels.append(datetime.strftime(date_temp, '%B'))
            liste_data.append(chiffre_affaire['sum_facture'])

        data_count[f"annee_{n}"] = liste_data_count
        labels[f"annee_{n}"] = liste_labels
        data[f"annee_{n}"] = liste_data
    
    context = {
        'nb_annees' : range(settings.ANNEES_MAX),
        'titre_annee' : today.year,
        'labels' : labels,
        'data' : data,
        'data_count' : data_count
    }
    return render(request, 'cabinet/chiffre_affaire.html', context)

def ordonnance_info(request, id):
    ordonnance = Ordonnance.objects.filter(id=id).first()
    liste_seances = Seance.objects.filter(ordonnance=ordonnance).filter(effectuee=True).order_by('-numero')
    seances_realisees = liste_seances.aggregate(seances_max=Count('numero',distinct=True))['seances_max']

    context = {
        'ordonnance' : ordonnance,
        'seances_realisees' : seances_realisees,
        'liste_seances' : liste_seances
    }
    return render(request, 'cabinet/ordonnance_informations.html', context)

def factures(request):
    total_factures = Facture.objects.annotate(year=ExtractYear('date_creation'),month=ExtractMonth('date_creation'),).values('year', 'month').annotate(sum_facture=Sum('montant')).order_by('-year', '-month')
    
    context = {
        'total_factures' : total_factures,
    }
    return render(request, 'cabinet/factures.html', context)

def factures_annee(request, annee):
    annee = int(annee)
    date_debut = datetime.strptime(f"{annee}-01-01", '%Y-%m-%d')
    date_fin = datetime.strptime(f"{annee}-12-31", '%Y-%m-%d')
    
    factures = Facture.objects.filter(date_creation__range=[date_debut, date_fin]).values('patient__nom','patient', 'paye').annotate(total_factures=Sum('montant')).order_by('-total_factures')
    
    context = {
        'factures' : factures,
        'annee': annee,
    }
    return render(request, 'cabinet/factures_annee.html', context)

def factures_mois(request, annee, mois):
    annee = int(annee)
    mois = int(mois)

    date_debut = datetime.strptime(f"{annee}-{mois}-01", '%Y-%m-%d')
    date_fin = datetime.strptime(f"{annee}-{mois}-{calendar._monthlen(annee, mois)}", '%Y-%m-%d')

    factures_periode = Facture.objects.filter(date_creation__range=[date_debut, date_fin])
    liste_factures = factures_periode.values('id', 'numero', 'patient__nom','patient', 'paye').annotate(total_factures=Sum('montant')).order_by('-total_factures')
    total_factures = factures_periode.aggregate(total_montant = Sum('montant'))['total_montant']

    context = {
        'liste_factures' : liste_factures,
        'total_factures' : total_factures,
        'annee': annee,
        'mois' : mois
    }
    return render(request, 'cabinet/factures_mois.html', context)

def facture_info(request, id):
    facture = get_object_or_404(Facture, id=id)
    
    context = {
        'facture' : facture,
    }
    return render(request, 'cabinet/facture_informations.html', context)   