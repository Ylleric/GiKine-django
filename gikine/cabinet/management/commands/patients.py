from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Patient, TypePatient
from django.conf import settings
import dbf

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01010.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    nomTypePatient = 'Patient' if line.TCP == 'P' else 'CNS'
                    typePatient = TypePatient.objects.get(nom = nomTypePatient)
                    
                    numero_compte = line.comt.rstrip('  ')
                    nom_patient = line.nom1.rstrip('  ')
                    matricule = int(line.malmat.rstrip('  ')) if line.malmat.rstrip('  ') != '' else None

                    rue = line.adr.rstrip('  ') if line.adr.rstrip('  ') != '' else None
                    code_postal = line.cptt.rstrip('  ') if line.cptt.rstrip('  ') != '' else None
                    ville = line.loc.rstrip('  ') if line.loc.rstrip('  ') != '' else None
                    telephone = line.tel.rstrip('  ') if line.tel.rstrip('  ') != '' else None
                    email = line.email.rstrip('  ') if line.email.rstrip('  ') != '' else None
                    sexe = line.sexe.rstrip('  ') if line.sexe.rstrip('  ') != '' else None

                    update_values= {
                        'typePatient' : typePatient,
                        'matricule': matricule, 
                        'rue': rue, 
                        'code_postal': code_postal, 
                        'ville': ville, 
                        'telephone': telephone, 
                        'email': email,
                        'sexe': sexe
                    }
                    
                    obj, create = Patient.objects.update_or_create(numero=numero_compte, nom=nom_patient, defaults=update_values)
                    obj.save()

            table.close()
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table patients"))