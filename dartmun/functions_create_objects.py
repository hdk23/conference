from .models import *
from django_countries import countries
from django.contrib.auth.models import User
import random

indices = random.sample(list(range(len(countries))), len(countries))


def create_delegation(committee: Committee) -> Delegation:
    """creates a delegation for the test committee"""
    country_index = indices.pop()
    country = countries[country_index]
    user = User(first_name=country.name, last_name=committee.acronym, username=f"{committee.acronym.lower()}{country.name.lower()}".replace(" ", ""))
    user.save()
    delegate = Delegate(user=user)
    delegate.save()
    delegation = Delegation(country=country)
    delegation.save()
    delegation.delegates.add(delegate)
    delegation.save()
    score_manager = ScoreManager(delegation=delegation)
    score_manager.save()

    committee = Committee.objects.get(acronym="UNEP")
    for category in committee.tally_categories.all():
        category_score = TallyCategoryScore(category=category)
        category_score.save()
        score_manager.tally_category_scores.add(category_score)
        score_manager.save()
    committee.score_managers.add(score_manager)
    committee.save()

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
    for category in TallyCategory.objects.all():
        committee_tally_category = CommitteeTallyCategory(category=category)
        committee_tally_category.save()
        committee.tally_categories.add(committee_tally_category)
    for num in range(40):
        committee.delegations.add(create_delegation(committee))
    committee.save()


def reset_committee():
    Committee.objects.all().delete()
    Chair.objects.all().delete()
    Delegation.objects.all().delete()
    Delegate.objects.all().delete()
    TallyGroup.objects.all().delete()
    TallyCategory.objects.all().delete()
    CommitteeTallyCategory.objects.all().delete()
    TallyScore.objects.all().delete()
    ScoreManager.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
