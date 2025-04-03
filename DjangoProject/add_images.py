import os
import django
import requests
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_salles.settings')
django.setup()

# Importer le modèle Salle
from reservations.models import Salle

# Créer le répertoire media/salles s'il n'existe pas
media_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'salles')
os.makedirs(media_dir, exist_ok=True)

# Liste des mots-clés pour les images
keywords = [
    'meeting room',
    'conference room',
    'coworking space',
    'training room',
    'office space'
]

# Fonction pour télécharger une image aléatoire
def download_random_image(keyword):
    try:
        # Utiliser l'API Unsplash pour obtenir une image aléatoire
        response = requests.get(f'https://source.unsplash.com/random/800x600/?{keyword}')
        if response.status_code == 200:
            return BytesIO(response.content)
        return None
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image: {e}")
        return None

# Ajouter des images aux salles
salles = Salle.objects.all()
for i, salle in enumerate(salles):
    # Utiliser un mot-clé correspondant à la salle ou un mot-clé par défaut
    keyword = keywords[i % len(keywords)]
    
    # Télécharger une image aléatoire
    image_data = download_random_image(keyword)
    
    if image_data:
        # Créer un nom de fichier unique
        filename = f"{salle.nom.lower().replace(' ', '_')}_{i}.jpg"
        
        # Sauvegarder l'image
        salle.image.save(filename, ContentFile(image_data.getvalue()), save=True)
        print(f"Image ajoutée à la salle '{salle.nom}'")
    else:
        print(f"Impossible d'ajouter une image à la salle '{salle.nom}'")

print("Toutes les images ont été ajoutées avec succès.") 