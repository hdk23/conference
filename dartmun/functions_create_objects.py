from .models import *
from django_countries import countries
from django.contrib.auth.models import User
import random

indices = random.sample(list(range(len(countries))), len(countries))


def create_delegation(committee: Committee, country=None) -> Delegation:
    """creates and returns a Delegation object"""
    if country is None:
        country_index = indices.pop()
        country = countries[country_index]
    user = User(first_name=country.name, last_name=committee.acronym,
                username=f"{committee.acronym.lower()}{country.name.lower()}".replace(" ", ""))
    user.save()
    delegate = Delegate(user=user)
    delegate.save()
    delegation = Delegation(country=country)
    delegation.save()
    delegation.delegates.add(delegate)
    delegation.save()
    return delegation


def add_rubric(committee: Committee, score_manager: ScoreManager, category_acronym: str, title: str, topic=None):
    """adds rubric entry for position paper/participation"""
    category = TallyCategory.objects.get(acronym=category_acronym)
    committee_category = committee.grades.tally_categories.get(category=category)
    rubric = Rubric.objects.get(title=title)
    rubric_entry = RubricEntry(rubric=rubric)
    if topic:
        rubric_entry.topic = topic
    rubric_entry.save()
    rubric_entry.set_rubric()
    tally = TallyScore(delegation=score_manager.delegation, category=category, rubric=rubric_entry, comments="")
    tally.save()
    score_manager.tally_category_scores.get(category=committee_category).add_tally(tally)
    committee.grades.add_tally(tally)
    committee.grades.save()


def initialize_delegation(committee: Committee, delegation=None) -> Delegation:
    """creates a delegation for the test committee"""
    # initialize delegation and score manager
    if delegation is None:
        delegation = create_delegation(committee)
    score_manager = ScoreManager(delegation=delegation)
    score_manager.save()

    # create tally category scores
    for category in committee.grades.tally_categories.all():
        category_score = TallyCategoryScore(delegation=delegation, category=category)
        category_score.save()
        score_manager.tally_category_scores.add(category_score)
        score_manager.save()
    committee.grades.score_managers.add(score_manager)
    committee.save()

    # position papers
    for topic in committee.topics.all():
        add_rubric(committee, score_manager, "PP", "Position Paper Rubric", topic)

    # participation
    add_rubric(committee, score_manager, "P", "Participation Rubric")
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
        rubrics = Rubric.objects.filter(tally_category=category)
        for rubric in rubrics:
            if category.acronym == "PP":
                for topic in committee.topics.all():
                    committee_tally_category.add_points_possible(rubric.max_possible)
            else:
                committee_tally_category.add_points_possible(rubric.max_possible)

    # add delegates
    for num in range(40):
        committee.people.delegations.add(initialize_delegation(committee))
        committee.people.save()
    committee.people.set_quorum()
    committee.save()


def reset_committee():
    """resets committee by deleting all objects except for the superuser"""
    Committee.objects.all().delete()
    Chair.objects.all().delete()
    Delegation.objects.all().delete()
    Delegate.objects.all().delete()
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
    Amendment.objects.all().delete()
    WritingManager.objects.all().delete()
    SponSig.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
