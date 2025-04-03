from django.shortcuts import render, redirect, get_object_or_404
from .models import Salle, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, date, timedelta
from .forms import ReservationForm, SalleForm
from django.contrib.auth import logout
from django.core.exceptions import ValidationError

def liste_salles(request):
    salles = Salle.objects.filter(disponible=True)
    query = request.GET.get('q')
    if query:
        salles = salles.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(equipements__icontains=query)
        )
    
    paginator = Paginator(salles, 6)
    page = request.GET.get('page')
    salles = paginator.get_page(page)
    
    return render(request, 'reservations/liste_salles.html', {
        'salles': salles,
        'query': query
    })

def detail_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    reservations = Reservation.objects.filter(salle=salle, date__gte=date.today())
    return render(request, 'reservations/detail_salle.html', {
        'salle': salle,
        'reservations': reservations
    })

@login_required
def reserver_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utilisateur = request.user
            reservation.salle = salle  # Associer la salle avant la validation
            
            # Vérifier si la salle est disponible
            if not salle.disponible:
                messages.error(request, "Cette salle n'est pas disponible pour le moment.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si la date est dans le passé
            if reservation.date < date.today():
                messages.error(request, "La date de réservation ne peut pas être dans le passé.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si l'heure de fin est après l'heure de début
            if reservation.heure_fin <= reservation.heure_debut:
                messages.error(request, "L'heure de fin doit être après l'heure de début.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si le nombre de participants est valide
            if reservation.nombre_participants < 1:
                messages.error(request, "Le nombre de participants doit être d'au moins 1.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si le nombre de participants ne dépasse pas la capacité
            if reservation.nombre_participants > salle.capacite:
                messages.error(request, f"Le nombre de participants ({reservation.nombre_participants}) dépasse la capacité de la salle ({salle.capacite}).")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier les chevauchements manuellement
            overlapping = Reservation.objects.filter(
                salle=salle,
                date=reservation.date,
                heure_debut__lt=reservation.heure_fin,
                heure_fin__gt=reservation.heure_debut
            ).exists()
            
            if overlapping:
                messages.error(request, "Cette salle est déjà réservée pour cette période.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Si toutes les validations sont passées, sauvegarder la réservation
            try:
                reservation.save()
                messages.success(request, "La réservation a été effectuée avec succès!")
                return redirect('reservations:mes_reservations')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/reserver_salle.html', {
        'form': form,
        'salle': salle
    })

@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(utilisateur=request.user).order_by('-date', '-heure_debut')
    return render(request, 'reservations/mes_reservations.html', {
        'reservations': reservations
    })

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    if reservation.date > date.today():
        reservation.statut = 'annulee'
        reservation.save()
        messages.success(request, "La réservation a été annulée avec succès.")
    else:
        messages.error(request, "Impossible d'annuler une réservation passée.")
    return redirect('reservations:mes_reservations')

@login_required
def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    salle = reservation.salle
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated_reservation = form.save(commit=False)
            
            # Vérifier si la salle est disponible
            if not salle.disponible:
                messages.error(request, "Cette salle n'est pas disponible pour le moment.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si la date est dans le passé
            if updated_reservation.date < date.today():
                messages.error(request, "La date de réservation ne peut pas être dans le passé.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si l'heure de fin est après l'heure de début
            if updated_reservation.heure_fin <= updated_reservation.heure_debut:
                messages.error(request, "L'heure de fin doit être après l'heure de début.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si le nombre de participants est valide
            if updated_reservation.nombre_participants < 1:
                messages.error(request, "Le nombre de participants doit être d'au moins 1.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier si le nombre de participants ne dépasse pas la capacité
            if updated_reservation.nombre_participants > salle.capacite:
                messages.error(request, f"Le nombre de participants ({updated_reservation.nombre_participants}) dépasse la capacité de la salle ({salle.capacite}).")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Vérifier les chevauchements manuellement (en excluant la réservation actuelle)
            overlapping = Reservation.objects.filter(
                salle=salle,
                date=updated_reservation.date,
                heure_debut__lt=updated_reservation.heure_fin,
                heure_fin__gt=updated_reservation.heure_debut
            ).exclude(id=reservation_id).exists()
            
            if overlapping:
                messages.error(request, "Cette salle est déjà réservée pour cette période.")
                return redirect('reservations:detail_salle', salle_id=salle.id)
            
            # Si toutes les validations sont passées, sauvegarder la réservation
            try:
                updated_reservation.save()
                messages.success(request, "La réservation a été modifiée avec succès!")
                return redirect('reservations:mes_reservations')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue: {str(e)}")
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'reservations/modifier_reservation.html', {
        'form': form,
        'reservation': reservation
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('reservations:liste_salles')
