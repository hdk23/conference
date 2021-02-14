from django.db import models
from .models_people import *
from .models_score import *
from .models_tally import *
import numpy as np


# Create your models here.
class Committee(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=8)

    directors = models.ManyToManyField(Chair, related_name="directors")
    managers = models.ManyToManyField(Chair, related_name="managers")
    delegations = models.ManyToManyField(Delegation)

    @staticmethod
    def set_normal():
        """
        sets the values for stats with tally category scores
        runs whenever a chair loads the committee scores page
        """
        for category in TallyCategory.objects.all():
            category_scores = TallyCategoryScore.objects.filter(category=category)
            category_scores = [score.raw_score for score in category_scores]
            category.stdev = np.std(category_scores)
            category.average = np.average(category_scores)
            category.save()

    def __str__(self):
        return f"{self.name} ({self.acronym})"
