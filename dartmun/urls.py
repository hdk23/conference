from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # My Committee Page URLs
    path('my_committee/', views.my_committee, name='my_committee'),
    path('my_committee/add_tally/', views.add_tally, name='add_tally'),
    path('my_committee/add_speech_entry/', views.add_speech_entry, name='add_speech_entry'),
    path('my_committee/remove_speech_entry/<int:id>', views.remove_speech_entry, name='remove_speech_entry'),
    path('my_committee/add_motion_entry/', views.add_motion_entry, name='add_motion_entry'),
    path('my_committee/remove_motion_entry/<int:id>', views.remove_motion_entry, name='remove_motion_entry'),
    path('my_committee/set_mod_speaker/<str:order>', views.set_mod_speaker, name='set_mod_speaker'),
    path('my_committee/vote_motion/', views.vote_motion, name='vote_motion'),
    path('my_committee/remove_motion_entry/<int:id>', views.remove_motion_entry, name='remove_motion_entry'),
    path('my_committee/update_attendance/', views.update_attendance, name='update_attendance'),
    path('my_committee/ssl/', views.ssl, name='ssl'),
    path('my_committee/add_amendment/', views.add_amendment, name='add_amendment'),

    # Other Page URLs
    path('grades/', views.grades, name='grades'),
    path('tallies/', views.tallies, name='tallies'),
    path('tallies/remove_tally/<int:id>', views.remove_tally, name='remove_tally'),
    path('pospapers/', views.pospapers, name='pospapers'),
    path('pospapers/<int:id>', views.delegation_papers, name='delegation_papers'),
    path('pospapers/update_paper/<int:id>', views.update_paper, name='update_paper'),
    path('resos', views.resos, name='resos'),
    path('resos/add_wp', views.add_wp, name='add_wp'),
    path('resos/remove_wp/<int:id>', views.remove_wp, name='remove_wp'),
    path('resos/add_reso', views.add_reso, name='add_reso'),
    path('resos/update_participation', views.update_participation, name='update_participation'),
]
