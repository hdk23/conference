from .models_people import *
from .models_score import *
from .models_tally import *
from .models_parli_pro import *
from .models_rubric import *
from .models_writing import *
from .models_grades_manager import GradesManager
from .models_parlipro_manager import ParliProManager
from .models_caucus_manager import CaucusManager


# Create your models here.
class Committee(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=8)
    topics = models.ManyToManyField(Topic)
    people = models.OneToOneField(PeopleManager, null=True, on_delete=models.CASCADE)
    grades = models.OneToOneField(GradesManager, null=True, on_delete=models.CASCADE)
    parli_pro = models.OneToOneField(ParliProManager, null=True, on_delete=models.CASCADE)
    writing = models.OneToOneField(WritingManager, null=True, on_delete=models.CASCADE)

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

    def initialize_delegation(self, country, responses):
        """initializes a delegation with the necessary managers"""
        delegation = self.people.add_delegation(country, responses)
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

    def __str__(self):
        return f"{self.name} ({self.acronym})"
