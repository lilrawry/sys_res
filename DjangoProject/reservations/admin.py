from django.contrib import admin
from .models import Salle, Reservation

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite', 'disponible', 'prix_par_heure')
    list_filter = ('disponible',)
    search_fields = ('nom', 'description', 'equipements')
    list_editable = ('disponible', 'prix_par_heure')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'salle', 'date', 'heure_debut', 'heure_fin', 'statut')
    list_filter = ('statut', 'date', 'salle')
    search_fields = ('utilisateur__username', 'salle__nom', 'motif')
    date_hierarchy = 'date'
    list_editable = ('statut',)
