from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Ordonnance, Patient, Medecin
from django.conf import settings
import dbf
from zipfile import ZipFile 

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01090.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    try:
                        numero_ordonnance = int(line.docnum)
                    except:
                        numero_ordonnance = None

                    try:
                        medecin = Medecin.objects.filter(matricule=int(line.toubib1)).first()
                    except:
                        medecin = None

                    try:
                        patient = Patient.objects.filter(numero=int(line.comt)).first()
                    except:
                        patient = None

                    description = line.causettt.rstrip('  ')
                    autorisation = line.titre.rstrip('  ')

                    date_prescription = line.docdate
                    date_validite = line.validite

                    date_cns_envoi = line.ucmenvoi
                    date_cns_retour = line.ucmretour

                    prestations_max_semaine = int(line.semseance)

                    update_values= {
                        'numero': numero_ordonnance, 
                        'medecin': medecin, 
                        'patient': patient, 
                        'description': description, 
                        'autorisation': autorisation, 
                        'prestations_max_semaine': prestations_max_semaine,
                        'date_prescription': date_prescription,
                        'date_fin_validite': date_validite,
                        'date_cns_envoi': date_cns_envoi,
                        'date_cns_retour': date_cns_retour,
                    }
                    
                    if numero_ordonnance and numero_ordonnance != 20000001:
                        obj, create = Ordonnance.objects.update_or_create(numero=numero_ordonnance, defaults=update_values)
                        obj.save()

            table.close()
        except Exception as e:
            self.stdout.stderr(f"{e}")


        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01097.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            
            zip_source_path = f"{settings.GI_PATH}/GI/ORD01/XML001"
            zip_destination_path = f"{settings.MEDIA_ROOT}/ordonnances"

            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    numero_autorisation = line.titre.rstrip('  ')

                    try:
                        ordonnance = Ordonnance.objects.filter(autorisation = numero_autorisation).first()
                    except:
                        ordonnance = None

                    taux = float(line.taux1)
                    prestations_max = int(line.nb1)
                    statut = True if line.accord.rstrip('  ') == 'ACC' else False
                    anomalie = line.anomalies.rstrip('  ')
                    
                    fichier_part_1, fichier_part_2, _, _, fichier_part_5, fichier_part_6, _ = line.fichier.rstrip('  ')[:-4].split('_')
                    fichier_zip = f"{line.fichier.rstrip('  ')[:-4]}.ZIP".replace("RETAUT_001", "DEMAUT_01")
                    fichier_pdf=f"{fichier_part_1}_{fichier_part_2}_DEMAUT_01_{fichier_part_5}_{fichier_part_6[4:]}.PDF"

                    try:
                        with ZipFile(f"{zip_source_path}/{fichier_zip}") as zf:
                            zf.extract(member=fichier_pdf, path=zip_destination_path)
                    except:
                        self.stdout.write(self.style.ERROR(f"Erreur avec le fichier {fichier_zip}"))
                        fichier_pdf = None

                    update_values = {
                        'prestations_max': prestations_max,
                        'statut': statut,
                        'anomalie': anomalie,
                        'fichier': fichier_pdf,
                        'taux': taux,
                    }
                    
                    if ordonnance:
                        obj, create = Ordonnance.objects.update_or_create(autorisation = numero_autorisation, defaults=update_values)
                        obj.save()
            table.close()
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table ordonnances"))