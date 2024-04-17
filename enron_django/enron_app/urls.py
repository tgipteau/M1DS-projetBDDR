from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.accueil, name="accueil"),
    path('employees', views.employees_table, name="employees_table"),
    path('', views.accueil, name="accueil"),
    path('thresholdsort', views.threshold_sort, name = 'threshold_sort'),
    path('showmessage', views.show_message, name = "show_message")
]
