from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Prestation, Ordonnance, Patient, Kinesitherapeute, TypePatient, Seance
from django.conf import settings
import dbf
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01091.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    numero_seance = int(line.prestnum)
                    libelle = line.libelle

                    try:
                        patient = Patient.objects.filter(numero=int(line.comt)).first()
                    except:
                        patient = None
                    
                    try:
                        kinesitherapeute = Kinesitherapeute.objects.filter(initiale=line.prestat.rstrip(' ')).first()
                    except:
                        kinesitherapeute = None

                    try:
                        ordonnance = Ordonnance.objects.filter(numero=int(line.docnum)).first()
                    except:
                        ordonnance  = None
                    
                    date_seance = line.prestdate
                    date_facture = line.factdate

                    code_prestation = line.prestfact

                    effectuee = True if line.exec == '+' else False
                    
                    update_values= {
                        'kinesitherapeute': kinesitherapeute,
                        'ordonnance':ordonnance, 
                        'libelle': libelle,
                        'patient': patient,
                        'code_prestation' : code_prestation,
                        'date_seance': date_seance,
                        'date_facture': date_facture,
                        'effectuee' : effectuee
                    }

                    obj, create = Seance.objects.update_or_create(numero=numero_seance, defaults=update_values)
                    obj.save()
            table.close()
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table seance"))