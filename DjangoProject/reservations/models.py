from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, date, time


class Salle(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    capacite = models.IntegerField()
    description = models.TextField(blank=True)
    equipements = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    image = models.ImageField(upload_to='salles/', blank=True, null=True)
    prix_par_heure = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"


class Reservation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    motif = models.TextField(blank=True)
    nombre_participants = models.IntegerField(default=1)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
        ('terminee', 'Terminée')
    ], default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.salle.nom} ({self.date} {self.heure_debut}-{self.heure_fin})"

    def clean(self):
        if self.date < date.today():
            raise ValidationError("La date de réservation ne peut pas être dans le passé.")
        
        if self.heure_fin <= self.heure_debut:
            raise ValidationError("L'heure de fin doit être après l'heure de début.")
        
        # Vérifier les chevauchements
        overlapping = Reservation.objects.filter(
            salle=self.salle,
            date=self.date,
            heure_debut__lt=self.heure_fin,
            heure_fin__gt=self.heure_debut
        ).exclude(id=self.id).exists()
        
        if overlapping:
            raise ValidationError("Cette salle est déjà réservée pour cette période.")

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date', '-heure_debut']
