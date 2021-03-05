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
    for category in committee.grades.tally_categories.all():
        category_score = TallyCategoryScore(category=category)
        category_score.save()
        score_manager.tally_category_scores.add(category_score)
        score_manager.save()
    committee.grades.score_managers.add(score_manager)
    committee.save()
    rubric = Rubric.objects.get(title="Position Paper Rubric")
    for topic in committee.topics.all():
        rubric_entry = RubricEntry(rubric=rubric, topic=topic)
        rubric_entry.save()
        for criterion in rubric.criteria.all():
            criterion_score = CriterionScore(criterion=criterion)
            criterion_score.save()
            rubric_entry.criterion_scores.add(criterion_score)
            rubric_entry.save()
        paper_category = TallyCategory.objects.get(acronym="PP")
        paper = TallyScore(delegation=delegation, category=paper_category, rubric=rubric_entry)
        paper.save()
        committee_category = CommitteeTallyCategory.objects.get(category=paper_category)
        score_manager.tally_category_scores.get(category=committee_category).add_tally(paper)
        score_manager.save()
    return delegation


def create_committee():
    """creates a test committee"""
    committee = Committee(name="United Nations Environmental Programme", acronym="UNEP")
    committee.save()
    indices = random.sample(list(range(len(countries))), len(countries))

    # initialize managers
    people_manager = PeopleManager()
    people_manager.save()
    grades_manager = GradesManager()
    grades_manager.save()
    parli_pro_manager = ParliProManager()
    parli_pro_manager.save()
    writing_manager = WritingManager()
    writing_manager.save()
    caucus_manager = CaucusManager()
    caucus_manager.save()
    committee.people = people_manager
    committee.grades = grades_manager
    committee.parli_pro = parli_pro_manager
    committee.parli_pro.caucus = caucus_manager
    committee.parli_pro.save()
    committee.writing = writing_manager
    committee.save()





    topic1 = Topic(topic="Air Pollution in Southeast Asia", number=1)
    topic2 = Topic(topic="Managing Outdated Nuclear Facilities", number=2)
    topic1.save()
    topic2.save()
    committee.topics.add(topic1)
    committee.topics.add(topic2)
    committee.save()

    # test committee with one chair
    chair = Chair(user=User.objects.get(username="henrykim"))
    chair.save()
    director = CommitteeDirector(chair=chair)
    director.save()
    committee.people.directors.add(director)

    # initialize tally categories for committee
    for category in TallyCategory.objects.all():
        committee_tally_category = CommitteeTallyCategory(category=category)
        committee_tally_category.save()
        committee.grades.tally_categories.add(committee_tally_category)

    # add delegates
    for num in range(40):
        committee.people.delegations.add(create_delegation(committee))
        committee.people.save()
    committee.people.set_quorum()
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
    GradesManager.objects.all().delete()
    PeopleManager.objects.all().delete()
    ParliProManager.objects.all().delete()
    CaucusManager.objects.all().delete()
    Motion.objects.all().delete()
    MotionEntry.objects.all().delete()
    SpeechEntry.objects.all().delete()
    DebateMode.objects.all().delete()
    Topic.objects.all().delete()
    Descriptor.objects.all().delete()
    Criterion.objects.all().delete()
    CriterionScore.objects.all().delete()
    Rubric.objects.all().delete()
    RubricEntry.objects.all().delete()
    WorkingPaper.objects.all().delete()
    Resolution.objects.all().delete()
    WritingManager.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
