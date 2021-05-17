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
    path('my_committee/reset_wp/', views.reset_wp, name='reset_wp'),
    path('my_committee/reset_reso/', views.reset_reso, name='reset_reso'),
    path('my_committee/reset_amend/', views.reset_amend, name='reset_amend'),
    path('my_committee/substantive_vote/', views.substantive_vote, name='substantive_vote'),

    # Other Page URLs
    path('about_committee/<str:committee_acronym>', views.about_committee, name='about_committee'),
    path('secretariat/', views.secretariat, name='secretariat'),
    path('admin/', views.admin, name='admin'),
    path('admin/add_delegation', views.add_delegation, name='add_delegation'),
    path('admin/manage_delegation/<int:id>', views.manage_delegation, name='manage_delegation'),
    path('attendance/', views.attendance, name='attendance'),
    path('grades/', views.grades, name='grades'),
    path('pospapers/', views.pospapers, name='pospapers'),
    path('pospapers/<int:id>', views.delegation_papers, name='delegation_papers'),
    path('pospapers/update_paper/<int:id>', views.update_paper, name='update_paper'),
    path('tallies/', views.tallies, name='tallies'),
    path('tallies/remove_tally/<int:id>', views.remove_tally, name='remove_tally'),
    path('resos', views.resos, name='resos'),
    path('resos/add_wp', views.add_wp, name='add_wp'),
    path('resos/remove_wp/<int:id>', views.remove_wp, name='remove_wp'),
    path('resos/add_reso', views.add_reso, name='add_reso'),
    path('resos/<int:not_enough>', views.add_reso, name='add_reso'),
    path('resos/update_participation', views.update_participation, name='update_participation'),
    path('bio/', views.bio, name='bio'),

    # API URLs
    path('add_calendar_entries/', views.add_calendar_entries, name='add_calendar_entries'),
    path('checkout/', views.checkout, name='checkout'),
    path('webhook/', views.stripe_webhook),
    path('create_payment/', views.create_payment, name='create_payment'),

    # superuser URLs
    path('committees/<str:mode>', views.committees, name='committees'),
    path('my_committee/<str:committee_acronym>', views.my_committee, name='my_committee'),
    path('pospapers/<str:committee_acronym>', views.pospapers, name='pospapers'),
    path('pospapers/<str:committee_acronym>/<int:id>', views.delegation_papers, name='delegation_papers'),
    path('grades/<str:committee_acronym>', views.grades, name='grades'),
    path('resos/<str:committee_acronym>', views.resos, name='resos'),
    path('tallies/<str:committee_acronym>', views.tallies, name='tallies'),
    path('attendance/<str:committee_acronym>', views.attendance, name='attendance'),
    path('admin/<str:committee_acronym>', views.admin, name='admin'),
    path('admin/manage_delegation/<str:committee_acronym>/<int:id>', views.manage_delegation, name='manage_delegation'),
]

