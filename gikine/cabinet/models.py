from django.db import models


class Kinesitherapeute(models.Model):
    nom = models.CharField(max_length=100, db_index=True)
    initiale = models.CharField(max_length=2, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)

    retrocetion_cabinet = models.FloatField(blank=True, null=True)
    retrocetion_domicile = models.FloatField(blank=True, null=True)
    retrocetion_deplacement = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'Kinesitherapeute'
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom}"


class Patient(models.Model):
    typePatient = models.ForeignKey('TypePatient', related_name="typePatient", on_delete=models.CASCADE, null=True)
    numero = models.IntegerField(db_index=True)
    nom = models.CharField(max_length=300)
    sexe = models.CharField(max_length=1, blank=True, null=True)

    rue = models.CharField(max_length=300, blank=True, null=True)
    code_postal = models.CharField(max_length=30, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)

    telephone = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    matricule = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Patient'
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom}"



class Prestation(models.Model):
    numero = models.IntegerField(db_index=True)
    patient = models.ForeignKey('Patient', related_name="tiers_patient", on_delete=models.CASCADE)
    tiers = models.ForeignKey('Patient', related_name="tiers_payeur", on_delete=models.CASCADE, null=True)
    ordonnance = models.ForeignKey('Ordonnance', on_delete=models.CASCADE, null=True)
    kinesitherapeute = models.ForeignKey('Kinesitherapeute', on_delete=models.CASCADE, null=True)

    code_acte = models.CharField(max_length=7)
    libelle = models.CharField(max_length=300)

    code_diff = models.IntegerField(blank=True, null=True)

    prix_acte = models.FloatField(blank=True, null=True)
    quantite = models.IntegerField(blank=True, null=True)

    taux = models.FloatField(blank=True, null=True)
    tarif_patient = models.FloatField(blank=True, null=True)

    date_prestation = models.DateField(blank=True, null=True)
    periode = models.IntegerField(blank=True, null=True)
    date_periode = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Prestation'
        ordering = ['numero']

    def __str__(self):
        return f"{self.numero} {self.patient}"

class Medecin(models.Model):
    matricule = models.IntegerField(db_index=True)

    nom = models.CharField(max_length=300)
    specialite = models.CharField(max_length=300)
    agreation = models.IntegerField(blank=True, null=True)

    rue = models.CharField(max_length=300, blank=True, null=True)
    code_postal = models.CharField(max_length=30, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=16, blank=True, null=True)
    
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Medecin'
        ordering = ['nom', ]

    def __str__(self):
        return f"Dr {self.nom}"

class Ordonnance(models.Model):
    numero = models.IntegerField(db_index=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    medecin = models.ForeignKey('Medecin', on_delete=models.CASCADE, null=True)

    description = models.CharField(max_length=300, blank=True, null=True)
    prestations_max = models.IntegerField(blank=True, null=True)
    prestations_max_semaine = models.IntegerField(blank=True, null=True)
    taux = models.IntegerField(blank=True, null=True)

    date_prescription = models.DateField(blank=True, null=True)
    date_fin_validite = models.DateField(blank=True, null=True)
    date_cns_envoi = models.DateField(blank=True, null=True)
    date_cns_retour = models.DateField(blank=True, null=True)

    autorisation = models.CharField(max_length=16, blank=True, null=True)
    anomalie = models.CharField(max_length=300, blank=True, null=True)
    statut = models.BooleanField(default=True)

    fichier = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Ordonnance'
        ordering = ['numero', ]

    def __str__(self):
        return f"{self.numero}"


class Facture(models.Model):
    numero = models.IntegerField(db_index=True)
    date_creation = models.DateField()

    ordonnance = models.ForeignKey('Ordonnance', on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey('Patient', related_name="patient", on_delete=models.CASCADE, null=True)
    tiers = models.ForeignKey('Patient', related_name="cns_patient_tiers", on_delete=models.CASCADE, null=True)

    montant = models.FloatField()
    montant_paye = models.FloatField(blank=True, null=True)
    paye = models.BooleanField(blank=True, null=True)

    periode = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Facture'
        ordering = ['numero', ]

    def __str__(self):
        return f"{self.numero}"


class TypePatient(models.Model):
    nom = models.CharField(max_length=16, unique=True)

    class Meta:
        verbose_name = 'TypePatient'
        ordering = ['nom', ]

    def __str__(self):
        return f"{self.nom}"
