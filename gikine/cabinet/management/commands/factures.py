from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Ordonnance, Patient, TypePatient, Facture
from django.conf import settings
from datetime import datetime
import dbf

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01024.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    numero_facture = int(line.docnum)
                    nomTypePatient = 'Patient' if line.TCP == 'P' else 'CNS'
                    paye = True if line.pouracquit == 'O' or nomTypePatient == 'CNS' else False
                    montant = float(line.total)
                    date_creation = line.docdate

                    try:
                        ordonnance = Ordonnance.objects.filter(autorisation=line.factcomm[:15]).first()
                    except:
                        ordonnance  = None
                    
                    try:
                        numero_patient = int(line.comt)
                    except:
                        numero_patient = None

                    try:
                        typePatient = TypePatient.objects.filter(nom=nomTypePatient).first()
                        patient = Patient.objects.filter(numero=numero_patient, typePatient=typePatient).first()
                    except Exception as e:
                        self.stdout.write(f"{e}")
                        patient = None

                    try:
                        typePatient = TypePatient.objects.filter(nom='Patient').first()
                        tiers = Patient.objects.filter(numero=int(line.comtp), typePatient=typePatient).first()
                    except:
                        tiers = None
                        
                    try:
                        periode = datetime.strptime(f"{line.periode.rstrip('  ')[0:4]}-{line.periode.rstrip('  ')[4:6]}-01", '%Y-%m-%d')
                    except:
                        periode = None

                    try:
                        montant_paye = float(line.factacc)
                    except:
                        montant_paye = None

                    update_values= {
                        'numero' : numero_facture,
                        'ordonnance' : ordonnance, 
                        'patient': patient,
                        'tiers' : tiers,
                        'date_creation': date_creation,
                        'periode' : periode,
                        'montant' : montant,
                        'montant_paye' : montant_paye,
                        'paye': paye
                    }

                    obj, create = Facture.objects.update_or_create(numero=numero_facture, defaults=update_values)
                    obj.save()
            table.close()
            
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table factures"))