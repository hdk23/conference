from django.db import models
from .models_tally import *
import decimal
import numpy as np


# Create your models here.
class TallyCategoryScore(models.Model):
    category = models.ForeignKey(TallyCategory)
    tallies = models.ManyToManyField(Tally)
    raw_score = models.DecimalField(max_digits=4, decimal_places=2)
    zscore = models.DecimalField(max_digits=4, decimal_places=3)
    scaled_score = models.DecimalField(max_digits=5, decimal_places=2)

    def add_tally(self, tally: Tally):
        """adds tally to the delegate's tally category score"""
        self.tallies.add(tally)
        self.raw_score += tally.score
        self.save()

    def remove_tally(self, tally: Tally) -> Tally:
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
