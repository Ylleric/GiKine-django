from django.core.management.base import BaseCommand, CommandError
from cabinet.models import Kinesitherapeute
from django.conf import settings
import dbf


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01013.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    initiale = line.prestat.rstrip('  ')
                    nom = line.nom1
                    numero = line.agreation
                    
                    update_values= {
                        'nom' : nom, 
                        'numero': numero,
                    }

                    obj, create = Kinesitherapeute.objects.update_or_create(initiale=initiale, defaults=update_values)
                    obj.save()
            table.close()
            
        except Exception as e:
            self.stdout.stderr(f"{e}")
        
        try:
            table = dbf.Table(filename=f"{settings.GI_PATH}/GI01/GI01018.DBF", codepage='cp437')
            table.open(dbf.READ_ONLY)
            for line in table:
                if dbf.is_deleted(line):
                    continue
                else:
                    initiale = line.prestat.rstrip('  ')
                    retrocetion_cabinet = float(line.retrocab)
                    retrocetion_domicile = float(line.retrodom)
                    retrocetion_deplacement = float(line.retrodepl)

                    update_values= {
                        'retrocetion_cabinet' : retrocetion_cabinet, 
                        'retrocetion_domicile': retrocetion_domicile,
                        'retrocetion_deplacement': retrocetion_deplacement,
                    }

                    obj, create = Kinesitherapeute.objects.update_or_create(initiale=initiale, defaults=update_values)
                    obj.save()
            table.close()
            
        except Exception as e:
            self.stdout.stderr(f"{e}")
        else:
            self.stdout.write(self.style.SUCCESS(f"[GiKine] Fin de la mise à jour de la table kine"))