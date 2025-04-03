from django import forms
from .models import Reservation, Salle
from datetime import date

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'heure_debut', 'heure_fin', 'motif', 'nombre_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'motif': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')
        nombre_participants = cleaned_data.get('nombre_participants')

        if date and heure_debut and heure_fin:
            if heure_fin <= heure_debut:
                raise forms.ValidationError("L'heure de fin doit être après l'heure de début.")

        if nombre_participants and nombre_participants < 1:
            raise forms.ValidationError("Le nombre de participants doit être d'au moins 1.")

        return cleaned_data
    
    def save(self, commit=True):
        # Désactiver la validation du modèle lors de la sauvegarde
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'capacite', 'description', 'equipements', 'disponible', 'image', 'prix_par_heure']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'equipements': forms.Textarea(attrs={'rows': 4}),
        } 