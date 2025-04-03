from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.liste_salles, name='liste_salles'),
    path('salle/<int:salle_id>/', views.detail_salle, name='detail_salle'),
    path('salle/<int:salle_id>/reserver/', views.reserver_salle, name='reserver_salle'),
    path('mes-reservations/', views.mes_reservations, name='mes_reservations'),
    path('reservation/<int:reservation_id>/annuler/', views.annuler_reservation, name='annuler_reservation'),
    path('reservation/<int:reservation_id>/modifier/', views.modifier_reservation, name='modifier_reservation'),
    path('logout/', views.logout_view, name='logout'),
]