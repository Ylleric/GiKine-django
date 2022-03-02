from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Prestation, Ordonnance, Patient, Kinesitherapeute, TypePatient
from django.conf import settings
import dbf
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01022.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    try:
                        tarif_consultation = float(line.detprix)
                    except:
                        tarif_consultation = None

                    try:
                        kinesitherapeute = Kinesitherapeute.objects.filter(initiale=line.prestat.rstrip(' ')).first()
                    except:
                        kinesitherapeute = None

                    numero_prestation = int(line.prestnum)
                    code_acte = line.artcode.rstrip(' ')
                    libelle = line.artlib

                    if code_acte == 'MASSAGE':
                        ordonnance = None
                    else:
                        try:
                            ordonnance = Ordonnance.objects.filter(numero=int(line.ordnum)).first()
                        except:
                            ordonnance  = None

                    try:
                        tiers_patient = Patient.objects.filter(numero=int(line.comtp)).first()
                    except:
                        tiers_patient = None
                    
                    try:
                        nomTypePatient = 'Patient' if line.TCP == 'P' else 'CNS'
                        typePatient = TypePatient.objects.get(nom = nomTypePatient)

                        tiers_payeur = Patient.objects.filter(numero=int(line.comt), typePatient=typePatient).first()
                    except:
                        tiers_payeur = None
                    
                    date_prestation = line.datentree

                    try:
                        if line.periode.rstrip('  ')[4:6] == "13":
                            date_periode = datetime.strptime(f"{line.periode.rstrip('  ')[0:4]}-12-01", '%Y-%m-%d')
                        else:
                            date_periode = datetime.strptime(f"{line.periode.rstrip('  ')[0:4]}-{line.periode.rstrip('  ')[4:6]}-01", '%Y-%m-%d')
                    except:
                        date_periode = None
                    
                    try:
                        taux = float(line.taux)
                    except:
                        taux = None
                    
                    update_values= {
                        'kinesitherapeute': kinesitherapeute,
                        'ordonnance':ordonnance, 
                        'libelle': libelle,
                        'patient': tiers_patient,
                        'prix_acte': tarif_consultation,
                        'date_prestation': date_prestation,
                        'date_periode': date_periode,
                        'taux': taux
                    }

                    obj, create = Prestation.objects.update_or_create(numero=numero_prestation, tiers=tiers_payeur, code_acte=code_acte, defaults=update_values)
                    obj.save()
            table.close()
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table prestations"))