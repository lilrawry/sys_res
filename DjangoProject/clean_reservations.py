import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_salles.settings')
django.setup()

from reservations.models import Reservation

# Trouver et supprimer les réservations sans salle
orphaned_reservations = Reservation.objects.filter(salle__isnull=True)
count = orphaned_reservations.count()

if count > 0:
    print(f"Suppression de {count} réservation(s) orpheline(s)...")
    orphaned_reservations.delete()
    print("Réservations orphelines supprimées avec succès.")
else:
    print("Aucune réservation orpheline trouvée.") 