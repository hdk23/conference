from django.db import models
from .models_tally import *
from .models_people import Delegation, Chair
from .models_rubric import RubricEntry
from .models_parli_pro import Motion
import numpy as np


# Create your models here.
class TallyScore(models.Model):
    """Individual scores for a delegate's position paper, speech, participation, etc."""
    scorer = models.ForeignKey(Chair, null=True, on_delete=models.CASCADE)
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(TallyCategory, on_delete=models.CASCADE, blank=True, null=True)
    score = models.FloatField(null=True)
    time = models.PositiveSmallIntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    rubric = models.ForeignKey(RubricEntry, on_delete=models.CASCADE, blank=True, null=True)
    motion = models.ForeignKey(Motion, on_delete=models.CASCADE, blank=True, null=True)

    def set_rubric_score(self):
        """sets the rubric score as the tally entry's score"""
        self.rubric.calc_total()
        self.score = self.rubric.total_score
        self.save()

    def mark_late(self):
        """marks a position paper as late"""
        self.score = 0
        self.rubric.total_score = 0
        self.save()

    def __str__(self):
        return f"{self.category.name} ({self.score}) by {self.delegation}"


class TallyCategoryScore(models.Model):
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(CommitteeTallyCategory, on_delete=models.CASCADE)
    raw_score = models.FloatField(default=0)
    zscore = models.FloatField(blank=True, null=True)
    scaled_score = models.FloatField(blank=True, null=True)

    def add_tally(self, tally: TallyScore):
        """adds tally to the delegate's tally category score"""
        if tally.score:
            self.raw_score += tally.score
        self.save()

    def remove_tally(self, tally: TallyScore) -> TallyScore:
        """removes tally from the delegate's tally category score"""
        self.raw_score -= tally.score
        tally.delete()
        self.save()
        return tally

    @staticmethod
    def calc_zscore(raw_score: float, average: float, stdev: float) -> float:
        """calculates the delegation's tally category score's z-score used for calculating total score"""
        return (raw_score - average) / stdev

    def calc_tallies(self, committee_average=None, committee_stdev=None):
        """calculates tally category score based on delegation's tallies"""
        average = self.category.average
        stdev = self.category.stdev
        if self.category.category.scaled:
            if stdev:
                # prevent division-by-zero error
                self.zscore = self.calc_zscore(self.raw_score, average, stdev)
                if self.category.category.scaled:
                    self.scaled_score = round(committee_average + committee_stdev * self.zscore, 2)
                else:
                    self.scaled_score = None
        else:
            if self.category.points_possible:
                tallies = TallyScore.objects.filter(category=self.category.category, delegation=self.delegation)
                points_possible = self.category.points_possible
                for tally in tallies:
                    if tally.rubric.total_score is None:
                        points_possible -= tally.rubric.rubric.max_possible
                    if points_possible > 0:
                        self.scaled_score = round(100 * self.raw_score / points_possible, 2)
                    else:
                        self.scaled_score = None
                self.save()
        self.save()

    def update_tally(self, tally: TallyScore, old_score: float):
        """updates a tally with a new score"""
        if self.raw_score and old_score:
            self.raw_score -= old_score
        self.raw_score += tally.score
        self.save()
        self.calc_tallies()
        self.save()

    def reset(self):
        self.raw_score = None
        self.zscore = None
        self.scaled_score = None

    def __str__(self):
        return f"{self.delegation} {self.category}: {self.raw_score} pts"


class ScoreManager(models.Model):
    """
    Score Manager class that tracks a delegation's scores
    """
    delegation = models.OneToOneField(Delegation, on_delete=models.CASCADE, null=True)
    tally_category_scores = models.ManyToManyField(TallyCategoryScore)
    score = models.FloatField(blank=True, null=True)

    def calc_score(self):
        """totals the delegation's scores from each category using a dot product"""
        weights = []
        scores = []
        max_possible = 100
        for tally_category in self.tally_category_scores.all():
            if tally_category.scaled_score is not None:
                weights.append(tally_category.category.category.weight / 100)
                scores.append(tally_category.scaled_score)
            else:
                max_possible -= tally_category.category.category.weight
        if scores:
            self.score = round(np.dot(weights, scores) * 100 / max_possible, 2)
        self.save()

    def remove_score_manager(self):
        self.tally_category_scores.all().delete()
        self.delete()

    def reset(self):
        for tcs in self.tally_category_scores.all():
            tcs.reset()

    def __str__(self):
        return f"{self.delegation} Score Manager"


class Awards(models.Model):
    """awards class to handle awards in a committee"""
    best_delegate = models.ForeignKey(Delegation, on_delete=models.CASCADE, null=True, related_name="BD")
    outstanding_delegate = models.ForeignKey(Delegation, on_delete=models.CASCADE, null=True, related_name="OD")
    honorable_mention = models.ForeignKey(Delegation, on_delete=models.CASCADE, null=True, related_name="HM")

    def __str__(self):
        return "Awards"
