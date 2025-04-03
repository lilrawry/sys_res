import os
import django
import requests
from PIL import Image
from io import BytesIO

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_salles.settings')
django.setup()

from reservations.models import Salle

# Chemin vers le dossier media
media_dir = 'media/salles'
os.makedirs(media_dir, exist_ok=True)

# URLs des images pour chaque type de salle
IMAGE_URLS = {
    'réunion': 'https://images.unsplash.com/photo-1517502884422-41eaead166d4',
    'conférence': 'https://images.unsplash.com/photo-1517502884422-41eaead166d4',
    'formation': 'https://images.unsplash.com/photo-1517502884422-41eaead166d4',
    'coworking': 'https://images.unsplash.com/photo-1497366216548-37526070297c',
    'bureau': 'https://images.unsplash.com/photo-1497366216548-37526070297c'
}

def download_and_save_image(url, filepath):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img = img.resize((800, 600), Image.Resampling.LANCZOS)
            img.save(filepath, 'JPEG')
            return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image: {e}")
    return False

# Créer et ajouter des images pour chaque salle
for i, salle in enumerate(Salle.objects.all()):
    # Créer un nom de fichier unique pour l'image
    filename = f"{salle.nom.lower().replace(' ', '_')}_{i}.jpg"
    filepath = os.path.join(media_dir, filename)
    
    # Déterminer le type de salle et l'URL correspondante
    salle_type = next((key for key in IMAGE_URLS.keys() if key in salle.nom.lower()), 'bureau')
    image_url = IMAGE_URLS[salle_type]
    
    # Télécharger et sauvegarder l'image
    if download_and_save_image(image_url, filepath):
        # Associer l'image à la salle
        salle.image = f'salles/{filename}'
        salle.save()
        print(f"Image ajoutée à la salle '{salle.nom}'")
    else:
        print(f"Impossible d'ajouter l'image à la salle '{salle.nom}'")

print("Toutes les images ont été ajoutées avec succès.") 