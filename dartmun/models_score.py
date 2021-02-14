from django.db import models
from .models_tally import *
import decimal
import numpy as np


# Create your models here.
class Chair(models.Model):
    """
    Chair class that represents committee directors (CDs) and committee managers (CMs)
    Separate classes for CDs and CMs
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Chair {self.user.get_full_name()}"


class TallyScore(models.Model):
    """Individual scores for a delegate's position paper, speech, participation, etc."""
    timestamp = models.DateTimeField(auto_now_add=True)
    scorer = models.ForeignKey(Chair, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    time = models.PositiveSmallIntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tally ({self.score}) by {self.scorer}"


class TallyCategoryScore(models.Model):
    category = models.ForeignKey(TallyCategory, on_delete=models.CASCADE)
    tallies = models.ManyToManyField(TallyScore)
    raw_score = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    zscore = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    scaled_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def add_tally(self, tally: TallyScore):
        """adds tally to the delegate's tally category score"""
        self.tallies.add(tally)
        self.raw_score += tally.score
        self.save()

    def remove_tally(self, tally: TallyScore) -> TallyScore:
        """removes tally from the delegate's tally category score"""
        self.tallies.remove(tally)
        self.raw_score -= tally.score
        self.save()
        return tally

    @staticmethod
    def calc_zscore(raw_score: decimal, average: decimal, stdev: decimal) -> decimal:
        """calculates the delegation's tally category score's z-score used for calculating total score"""
        return (raw_score - average)/stdev

    def calc_tallies(self):
        """calculates tally category score based on delegation's tallies"""
        average = self.category.average
        stdev = self.category.stdev
        self.zscore = self.calc_zscore(self.raw_score, average, stdev)
        self.scaled_score = average + stdev * self.zscore
        self.save()

    def __str__(self):
        return f"{self.category}: {self.raw_score} pts"
