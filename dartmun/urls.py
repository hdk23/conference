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
    path('add_speech_entry/', views.add_speech_entry, name='add_speech_entry'),
    path('remove_speech_entry/<int:id>', views.remove_speech_entry, name='remove_speech_entry'),
    path('add_motion_entry/', views.add_motion_entry, name='add_motion_entry'),
    path('remove_motion_entry/<int:id>', views.remove_motion_entry, name='remove_motion_entry'),
    path('set_mod_speaker/<str:order>', views.set_mod_speaker, name='set_mod_speaker'),
    path('vote_motion/', views.vote_motion, name='vote_motion'),
    path('update_attendance/', views.update_attendance, name='update_attendance'),
]