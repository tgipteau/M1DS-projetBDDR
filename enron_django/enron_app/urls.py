from django.urls import path
from . import views

urlpatterns = [
    path('accueil', views.accueil, name="accueil"),
    path('employees', views.employees_table, name="employees_table"),
    path('', views.accueil, name="accueil"),
    path('basicmining', views.basic_mining, name = 'basic_mining'),
    path('message/<int:message_id>/', views.show_message, name = "show_message"),
    path('seuils', views.seuils, name = 'seuils'),
    path('interactions', views.interactions, name = 'interactions'),
    path('conversation/<int:employee_a_id>-<int:employee_b_id>/', views.conversation, name = 'conversation'),
    path('achalandage', views.achalandage, name = 'achalandage'),
]
