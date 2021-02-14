from .models import Delegate, Delegation, Committee, Chair, CommitteeDirector
from django_countries import countries
from django.contrib.auth.models import User
import random

indices = random.sample(list(range(len(countries))), len(countries))


def create_delegation() -> Delegation:
    """creates a delegation for the test committee"""
    country_index = indices.pop()
    country = countries[country_index]
    user = User(first_name=country.name, last_name="UNEP", username=f"unep{country.name.lower()}".replace(" ", ""))
    user.save()
    delegate = Delegate(user=user)
    delegate.save()
    delegation = Delegation(country=country)
    delegation.save()
    delegation.delegates.add(delegate)
    delegation.save()
    return delegation


def create_committee():
    """creates a test committee"""
    committee = Committee(name="United Nations Environmental Programme", acronym="UNEP")
    committee.save()
    chair = Chair(user=User.objects.get(username="henrykim"))
    chair.save()
    director = CommitteeDirector(chair=chair)
    director.save()
    committee.directors.add(director)
    for num in range(40):
        committee.delegations.add(create_delegation())
    committee.save()


def reset_committee():
    Committee.objects.all().delete()
    Chair.objects.all().delete()
    Delegation.objects.all().delete()
    Delegate.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
