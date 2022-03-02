from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Medecin
from django.conf import settings
import dbf

class Command(BaseCommand):
    def handle(self, *args, **kwargs):        
        try:    
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01011.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    try:
                        matricule = int(line.toubib)
                    except:
                        matricule = None

                    try:
                        agreation = int(line.tagreation)
                    except:
                        agreation = None
                    
                    nom_medecin = line.tnom1.rstrip('  ')
                    specialite = line.tnom2.rstrip('  ')
                    
                    adresse_rue = line.tadr.rstrip('  ') if line.tadr.rstrip('  ') != '' else None
                    adresse_code_postal = line.tcptt.rstrip('  ') if line.tcptt.rstrip('  ') != '' else None
                    adresse_ville = line.tloc.rstrip('  ') if line.tloc.rstrip('  ') != '' else None
                    numero_telephone = line.ttel.rstrip('  ') if line.ttel.rstrip('  ') != '' else None
                    actif = True if line.actif.rstrip('  ') == 'O' else False

                    update_values= {
                        'nom': nom_medecin, 
                        'specialite': specialite, 
                        'rue': adresse_rue, 
                        'code_postal': adresse_code_postal, 
                        'ville': adresse_ville, 
                        'telephone': numero_telephone,
                        'agreation': agreation,
                        'actif': actif
                    }

                    if matricule:
                        obj, create = Medecin.objects.update_or_create(matricule=matricule, defaults=update_values)
                        obj.save()

            table.close()
            
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table medecins"))