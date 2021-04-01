from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TallyCategory(models.Model):
    """Tally Category for scoring delegates"""
    name = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    weight = models.PositiveSmallIntegerField()
    scaled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.weight}%)"


class CommitteeTallyCategory(models.Model):
    """Committee Tally Category class for tracking committee category averages"""
    category = models.ForeignKey(TallyCategory, on_delete=models.CASCADE)
    average = models.FloatField(blank=True, null=True)
    scaled_average = models.FloatField(blank=True, null=True)
    stdev = models.FloatField(blank=True, null=True)
    points_possible = models.FloatField(default=0)

    def add_points_possible(self, points: float):
        """adds points to category points possible"""
        self.points_possible += points
        self.save()

    def reset(self):
        self.scaled_average = None
        self.scaled_average = None
        self.stdev = None
        self.points_possible = 0
        self.save()

    def __str__(self):
        return f"{self.category} Committee Tally Category"
