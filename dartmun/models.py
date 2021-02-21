from django.db import models
from .models_people import *
from .models_score import *
from .models_tally import *
from .models_grades_manager import GradesManager
import numpy as np


# Create your models here.
class Committee(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=8)
    people = models.ForeignKey(PeopleManager, null=True, on_delete=models.CASCADE)
    grades = models.ForeignKey(GradesManager, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.acronym})"
