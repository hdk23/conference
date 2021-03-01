from django.db import models
from .models_tally import TallyCategory
from .models_parli_pro import Topic


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
    max_possible = models.FloatField(default=0)

    def calc_total(self):
        """calculates the points possible for a rubric"""
        self.max_possible = 0
        for criterion in self.criteria.all():
            print(criterion.weight)
            self.max_possible += criterion.weight
        self.save()

    def __str__(self):
        return f"{self.title} ({self.tally_category})"


class CriterionScore(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    descriptor = models.ForeignKey(Descriptor, blank=True, null=True, on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.criterion}: {self.score} pts"


class RubricEntry(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    criterion_scores = models.ManyToManyField(CriterionScore)
    total_score = models.FloatField(blank=True, null=True)

    def calc_total(self):
        """calculates the points that an entry earns based on a rubric"""
        self.total_score = 0
        for criterion_score in self.criterion_scores.all():
            self.total_score += criterion_score.score
        self.save()

    def __str__(self):
        return f"{self.rubric}: {self.total_score}"
