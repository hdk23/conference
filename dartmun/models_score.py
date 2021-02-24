from django.db import models
from .models_tally import *
from .models_people import Delegation, Chair

import decimal
import numpy as np


# Create your models here.
class Descriptor(models.Model):
    descriptor = models.TextField()
    points = models.FloatField()

    def __str__(self):
        return f"{self.descriptor} - {self.points} pts"


class Criterion(models.Model):
    criterion = models.CharField(max_length=64)
    weight = models.IntegerField()
    possible_scores = models.ManyToManyField(Descriptor)

    def __str__(self):
        return f"{self.criterion}"


class Rubric(models.Model):
    title = models.CharField(max_length=64)
    tally_category = models.ForeignKey(TallyCategory, on_delete=models.CASCADE)
    criteria = models.ManyToManyField(Criterion)
    max_possible = models.FloatField()

    def calc_total(self):
        self.max_possible = 0
        for criterion in self.criteria.all():
            self.max_possible += criterion.weight
        self.save()

    def __str__(self):
        return f"{self.title} ({self.tally_category})"


class CriterionScore(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    descriptor = models.ForeignKey(Descriptor, blank=True, null=True, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.criterion}: {self.score} pts"


class RubricEntry(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    criterion_scores = models.ManyToManyField(CriterionScore)
    total_score = models.FloatField(blank=True, null=True)

    def calc_total(self):
        self.total_score = 0
        for criterion_score in self.criterion_scores.all():
            self.total_score += criterion_score.score
        self.save()

    def __str__(self):
        return f"{self.rubric}: {self.total_score}"


class TallyScore(models.Model):
    """Individual scores for a delegate's position paper, speech, participation, etc."""
    scorer = models.ForeignKey(Chair, on_delete=models.CASCADE)
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(TallyCategory, on_delete=models.CASCADE, blank=True, null=True)
    score = models.PositiveSmallIntegerField()
    time = models.PositiveSmallIntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} ({self.score}) by {self.delegation}"


class TallyCategoryScore(models.Model):
    category = models.ForeignKey(CommitteeTallyCategory, on_delete=models.CASCADE)
    tallies = models.ManyToManyField(TallyScore)
    raw_score = models.FloatField(default=0)
    zscore = models.FloatField(blank=True, null=True)
    scaled_score = models.FloatField(blank=True, null=True)

    def add_tally(self, tally: TallyScore):
        """adds tally to the delegate's tally category score"""
        self.raw_score += tally.score
        self.save()

    def remove_tally(self, tally: TallyScore) -> TallyScore:
        """removes tally from the delegate's tally category score"""
        print(self.raw_score)
        self.raw_score -= tally.score
        print(self.raw_score)
        tally.delete()
        self.save()
        print(self.raw_score)
        return tally

    @staticmethod
    def calc_zscore(raw_score: float, average: float, stdev: float) -> float:
        """calculates the delegation's tally category score's z-score used for calculating total score"""
        return (raw_score - average)/stdev

    def calc_tallies(self, committee_average: float, committee_stdev: float):
        """calculates tally category score based on delegation's tallies"""
        average = self.category.average
        stdev = self.category.stdev
        if stdev > 0:
            # prevent division-by-zero error
            self.zscore = self.calc_zscore(self.raw_score, average, stdev)
            self.scaled_score = round(committee_average + committee_stdev * self.zscore, 2)
            self.save()

    def __str__(self):
        return f"{self.category}: {self.raw_score} pts"


class ScoreManager(models.Model):
    """
    Score Manager class that tracks a delegation's scores
    """
    delegation = models.OneToOneField(Delegation, on_delete=models.CASCADE, null=True)
    tally_category_scores = models.ManyToManyField(TallyCategoryScore)
    score = models.FloatField(blank=True, null=True)

    def calc_score(self, max_possible):
        """totals the delegation's scores from each category using a dot product"""
        weights = []
        scores = []
        for tally_category in self.tally_category_scores.all():
            if tally_category.category.average > 0:
                weights.append(tally_category.category.category.weight / 100)
                scores.append(tally_category.scaled_score)
        self.score = round(np.dot(weights, scores) * 100 / max_possible, 2)
        self.save()

    def __str__(self):
        return f"{self.delegation} Score Manager"