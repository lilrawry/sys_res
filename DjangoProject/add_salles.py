import os
import django

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_salles.settings')
django.setup()

# Importer le modèle Salle
from reservations.models import Salle

# Liste des salles à ajouter
salles = [
    {
        'nom': 'Salle de réunion A',
        'capacite': 10,
        'description': 'Salle de réunion moderne avec vue panoramique',
        'equipements': 'Projecteur, écran, tableau blanc, connexion Wi-Fi',
        'prix_par_heure': 50.00,
        'disponible': True
    },
    {
        'nom': 'Salle de conférence B',
        'capacite': 30,
        'description': 'Grande salle de conférence avec système audio',
        'equipements': 'Microphones, haut-parleurs, projecteur, écran géant',
        'prix_par_heure': 100.00,
        'disponible': True
    },
    {
        'nom': 'Espace de coworking',
        'capacite': 20,
        'description': 'Espace ouvert pour le travail collaboratif',
        'equipements': 'Tables modulaires, connexion Wi-Fi, imprimante',
        'prix_par_heure': 30.00,
        'disponible': True
    },
    {
        'nom': 'Salle de formation',
        'capacite': 15,
        'description': 'Salle adaptée pour les formations et ateliers',
        'equipements': 'Tableaux interactifs, ordinateurs, connexion Wi-Fi',
        'prix_par_heure': 75.00,
        'disponible': True
    },
    {
        'nom': 'Bureau privé',
        'capacite': 4,
        'description': 'Bureau privé pour réunions confidentielles',
        'equipements': 'Table de réunion, connexion Wi-Fi, téléphone',
        'prix_par_heure': 40.00,
        'disponible': True
    }
]

# Ajouter les salles à la base de données
for salle_data in salles:
    salle, created = Salle.objects.get_or_create(
        nom=salle_data['nom'],
        defaults=salle_data
    )
    if created:
        print(f"Salle '{salle.nom}' créée avec succès.")
    else:
        print(f"La salle '{salle.nom}' existe déjà.")

print("Toutes les salles ont été ajoutées avec succès.") 