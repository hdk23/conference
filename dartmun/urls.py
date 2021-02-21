from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_committee/', views.my_committee, name='my_committee'),
    path('grades/', views.grades, name='grades'),
    path('tallies/', views.tallies, name='tallies'),
    path('grades/', views.grades, name='grades'),
    path('add_tally/', views.add_tally, name='add_tally'),
    path('remove_tally/<int:id>', views.remove_tally, name='remove_tally'),
]