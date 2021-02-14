from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_committee/', views.my_committee, name='my_committee'),
]