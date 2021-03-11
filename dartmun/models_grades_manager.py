from django.db import models
from .models_score import *
from .models_parli_pro import Topic
from .models_writing import Resolution


class GradesManager(models.Model):
    score_managers = models.ManyToManyField(ScoreManager)
    tally_categories = models.ManyToManyField(CommitteeTallyCategory)
    tallies = models.ManyToManyField(TallyScore)
    category_average = models.FloatField(default=87.5)
    category_stdev = models.FloatField(default=5)
    need_update = models.BooleanField(default=False)

    def set_normal(self):
        """
        sets the values for stats with tally category scores
        runs whenever a chair loads the committee scores page
        """

        for category in self.tally_categories.all():
            category_scores = TallyCategoryScore.objects.filter(category=category)
            category_scores = [score.raw_score for score in category_scores]
            category.stdev = np.std(category_scores)
            category.average = np.average(category_scores)
            category.save()

    def calc_grades(self):
        """calculates grades in the committee"""
        self.set_normal()  # normalize category scores

        # calculate tallies within each category
        for score_manager in self.score_managers.all():
            for tally_category_score in score_manager.tally_category_scores.all():
                tally_category_score.calc_tallies(self.category_average, self.category_stdev)

        # adjust the maximum possible score if not all categories have tallies
        max_possible = 100
        for committee_tally_category in self.tally_categories.all():
            if committee_tally_category.average <= 0:
                max_possible -= committee_tally_category.category.weight
        for score_manager in self.score_managers.all():
            score_manager.calc_score(max_possible)

        # set need_update back to false
        self.need_update = False

    def get_category_score(self, delegation: Delegation, category: TallyCategory) -> TallyCategoryScore:
        """retrieves a delegation's tally category score"""
        score_manager = self.score_managers.get(delegation=delegation)
        committee_category = self.tally_categories.get(category=category)
        category_score = score_manager.tally_category_scores.get(category=committee_category)
        return category_score

    def add_tally(self, tally: TallyScore):
        """adds tally to the committee records and increments the delegation's raw score"""
        self.tallies.add(tally)
        category_score = self.get_category_score(tally.delegation, tally.category)
        category_score.add_tally(tally)
        category_score.save()
        self.need_update = True
        self.save()

    def remove_tally(self, tally: TallyScore) -> TallyScore:
        """
        removes tally from committee records and decrements the delegation's raw score
        returns the tally just deleted
        """
        category_score = self.get_category_score(tally.delegation, tally.category)
        tally = category_score.remove_tally(tally)
        category_score.save()
        self.need_update = True
        self.save()
        return tally

    def update_tally(self, tally: TallyScore, new_score: float):
        """updates a tally's score based on a new value"""
        category_score = self.get_category_score(tally.delegation, tally.category)
        category_score.update_tally(tally, new_score)
        category_score.save()
        self.need_update = True
        self.save()

    def add_reso_grades(self, reso: Resolution, topic: Topic, rubric_entry: RubricEntry):
        """adds tally entries for rubric"""
        category = TallyCategory.objects.get(acronym="R")
        rubric_score = rubric_entry.total_score
        for sponsor in reso.sponsig.sponsors.all():
            tally = TallyScore(category=category, delegation=sponsor, score=rubric_score)
            tally.save()
            self.add_tally(tally)
        for signatory in reso.sponsig.signatories.all():
            tally = TallyScore(category=category, delegation=signatory, score=4)
            tally.save()
            self.add_tally(tally)
        for wp in topic.working_papers.all():
            for sponsor in wp.sponsig.sponsors.all():
                if sponsor not in reso.sponsig.sponsors.all() and sponsor not in reso.sponsig.signatories.all():
                    tally = TallyScore(category=category, delegation=sponsor, score=rubric_score/2)
                    tally.save()
                    self.add_tally(tally)
        self.save()

    def __str__(self):
        return f"Grades Manager"
