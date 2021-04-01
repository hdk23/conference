from django.db import models
from .models_score import *
from .models_parli_pro import Topic
from .models_tally import TallyCategory
from .models_writing import Resolution


class GradesManager(models.Model):
    score_managers = models.ManyToManyField(ScoreManager)
    tally_categories = models.ManyToManyField(CommitteeTallyCategory)
    tallies = models.ManyToManyField(TallyScore)
    awards = models.OneToOneField(Awards, on_delete=models.CASCADE, null=True)
    category_average = models.FloatField(default=87.5)
    category_stdev = models.FloatField(default=5)
    committee_average = models.FloatField(null=True, blank=True)
    need_update = models.BooleanField(default=False)

    def create_tally_categories(self):
        for category in TallyCategory.objects.all():
            committee_category = CommitteeTallyCategory(category=category)
            committee_category.save()
            if category.acronym == "PP":
                committee_category.add_points_possible(40)
            elif category.acronym == "R":
                committee_category.add_points_possible(20)
            self.tally_categories.add(committee_category)
            self.save()

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
                scores = []
                if tally_category_score.category.category.scaled:
                    tally_category_score.calc_tallies(self.category_average, self.category_stdev)
                else:
                    tally_category_score.calc_tallies()

        for score_manager in self.score_managers.all():
            score_manager.calc_score()

        self.calc_scaled_averages()

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
            tally = TallyScore(category=category, delegation=sponsor, score=rubric_score, comments="Reso Sponsor")
            tally.save()
            self.add_tally(tally)
        for signatory in reso.sponsig.signatories.all():
            tally = TallyScore(category=category, delegation=signatory, score=4, comments="Signatory")
            tally.save()
            self.add_tally(tally)
        for wp in topic.working_papers.all():
            for sponsor in wp.sponsig.sponsors.all():
                if sponsor not in reso.sponsig.sponsors.all() and sponsor not in reso.sponsig.signatories.all():
                    tally = TallyScore(category=category, delegation=sponsor, score=rubric_score/2, comments="WP Sponsor")
                    tally.save()
                    self.add_tally(tally)
        self.save()

    def calc_scaled_averages(self):
        """calculates the scaled average for each category"""
        for tally_category in self.tally_categories.all():
            if tally_category.category.scaled:
                tally_category.scaled_average = self.category_average
            else:
                scores = []
                for score_manager in self.score_managers.all():
                    score = score_manager.tally_category_scores.get(category=tally_category).scaled_score
                    if score:
                        scores.append(score)
                tally_category.scaled_average = round(np.average(scores), 2)
            tally_category.save()

        # calculate committee scaled average
        scores = []
        for score_manager in self.score_managers.all():
            scores.append(score_manager.score)
        try:
            self.committee_average = round(np.average(scores), 2)
        except TypeError:
            self.committee_average = None
        self.save()
        self.give_awards()

    def give_awards(self):
        """declares awardees for the top 3 scores"""
        to_give = self.score_managers.order_by('delegation__country').order_by('-score')[0:3]
        self.awards.best_delegate = to_give[0].delegation
        self.awards.outstanding_delegate = to_give[1].delegation
        self.awards.honorable_mention = to_give[2].delegation
        self.awards.save()

    def reset(self):
        """resets the grade manager"""
        for sm in self.score_managers.all():
            sm.reset()
        for tc in self.tally_categories.all():
            tc.reset()
        self.tallies.all().delete()
        self.category_average = 87.5
        self.category_stdev = 5
        self.committee_average = None
        self.need_update = False
        self.save()

    def __str__(self):
        return f"Grades Manager"
