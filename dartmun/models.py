from .models_people import *
from .models_score import *
from .models_tally import *
from .models_parli_pro import *
from .models_rubric import *
from .models_writing import *
from .models_logistics import Session
from .models_grades_manager import GradesManager
from .models_parlipro_manager import ParliProManager
from .models_people_manager import PeopleManager
from .models_caucus_manager import CaucusManager
from .models_writing_manager import WritingManager


# Create your models here.
class Committee(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=8)
    topics = models.ManyToManyField(Topic)
    current_session = models.ForeignKey(Session, null=True, on_delete=models.CASCADE)
    people = models.OneToOneField(PeopleManager, null=True, on_delete=models.CASCADE)
    grades = models.OneToOneField(GradesManager, null=True, on_delete=models.CASCADE)
    parli_pro = models.OneToOneField(ParliProManager, null=True, on_delete=models.CASCADE)
    writing = models.OneToOneField(WritingManager, null=True, on_delete=models.CASCADE)
    adjourned = models.BooleanField(default=False)

    def set_managers(self, double=False):
        self.current_session = conference.sessions.get(number=1)
        if not self.people:
            people_manager = PeopleManager(double_delegation=double)
            people_manager.save()
            self.people = people_manager
        if not self.grades:
            grades_manager = GradesManager()
            grades_manager.save()
            grades_manager.create_tally_categories()
            awards = Awards()
            awards.save()
            grades_manager.awards = awards
            grades_manager.save()
            self.grades = grades_manager
        if not self.parli_pro:
            parli_pro_manager = ParliProManager()
            parli_pro_manager.save()
            self.parli_pro = parli_pro_manager
            if not self.parli_pro.caucus:
                caucus_manager = CaucusManager()
                caucus_manager.save()
                self.parli_pro.caucus = caucus_manager
                self.parli_pro.save()
        if not self.writing:
            writing_manager = WritingManager()
            writing_manager.save()
            self.writing = writing_manager
        self.save()

    def has_wps(self):
        """determines whether the committee has resolutions submitted"""
        for topic in self.topics.all():
            if topic.working_papers.count():
                return True
        return False

    def has_resos(self):
        """determines whether the committee has resolutions submitted"""
        for topic in self.topics.all():
            if topic.resolutions.count():
                return True
        return False

    def add_rubric(self, score_manager: ScoreManager, category_acronym: str, title: str, topic=None):
        """adds a rubric entry for a new delegation"""
        category = TallyCategory.objects.get(acronym=category_acronym)
        committee_category = self.grades.tally_categories.get(category=category)
        rubric = Rubric.objects.get(title=title)
        rubric_entry = RubricEntry(rubric=rubric)
        if topic:
            rubric_entry.topic = topic
        rubric_entry.save()
        rubric_entry.set_rubric()
        tally = TallyScore(delegation=score_manager.delegation, category=category, rubric=rubric_entry, comments="")
        tally.save()
        score_manager.tally_category_scores.get(category=committee_category).add_tally(tally)
        self.grades.add_tally(tally)
        self.grades.save()

    def initialize_delegation(self, delegation: Delegation):
        """initializes a delegation with the necessary managers"""
        # initialize attendance records
        for session in conference.sessions.all():
            ar = AttendanceRecord(session=session)
            ar.save()
            delegation.attendance_records.add(ar)
            delegation.save()
        try:
            score_manager = ScoreManager.objects.get(delegation=delegation)
        except:
            score_manager = ScoreManager(delegation=delegation)
            score_manager.save()

        # create tally category scores
        for category in self.grades.tally_categories.all():
            category_score = TallyCategoryScore(delegation=delegation, category=category)
            category_score.save()
            score_manager.tally_category_scores.add(category_score)
            score_manager.save()
        self.grades.score_managers.add(score_manager)
        self.save()

        # position papers
        for topic in self.topics.all():
            self.add_rubric(score_manager, "PP", "Position Paper Rubric", topic)

        # participation
        self.add_rubric(score_manager, "P", "Participation Rubric")

        # add to committee
        return delegation

    def add_chair(self, user: User):
        """adds a chair to the committee"""
        self.people.add_user(user)

    def recess(self):
        """resets committee after motioning to recess"""
        try:
            self.current_session = conference.sessions.get(number=self.current_session.number + 1)
        except:
            pass  # declare winners?
        self.parli_pro.reset()
        self.parli_pro.save()
        self.people.reset()
        self.people.save()
        self.save()

    def adjourn(self):
        """adjourns committee"""
        self.adjourned = True
        self.grades.give_awards()
        self.grades.save()
        self.save()

    def __str__(self):
        return f"{self.name} ({self.acronym})"


class Organ(models.Model):
    """Organ model to hold several committees"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    committees = models.ManyToManyField(Committee)

    def __str__(self):
        return f"{self.name} ({self.acronym})"


class Conference(models.Model):
    """Conference model to hold organs and logistical info"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=16, null=True)
    organs = models.ManyToManyField(Organ)
    sessions = models.ManyToManyField(Session)
    secretariat = models.ManyToManyField(Secretariat)

    def add_secretariat(self, user: User, position: str, year: int, bio: str):
        """adds a secretariat member to the conference"""
        secretariat = Secretariat(user=user, position=position, year=year, bio=bio)
        secretariat.save()
        self.secretariat.add(secretariat)
        self.save()

    def __str__(self):
        return self.name

conference = Conference.objects.get(acronym="DartMUN 2021")