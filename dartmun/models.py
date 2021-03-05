from .models_people import *
from .models_score import *
from .models_tally import *
from .models_parli_pro import *
from .models_rubric import *
from .models_writing import *
from .models_grades_manager import GradesManager
from .models_parlipro_manager import ParliProManager
from .models_caucus_manager import CaucusManager


# Create your models here.
class Committee(models.Model):
    name = models.CharField(max_length=128)
    acronym = models.CharField(max_length=8)
    topics = models.ManyToManyField(Topic)
    people = models.OneToOneField(PeopleManager, null=True, on_delete=models.CASCADE)
    grades = models.OneToOneField(GradesManager, null=True, on_delete=models.CASCADE)
    parli_pro = models.OneToOneField(ParliProManager, null=True, on_delete=models.CASCADE)
    writing = models.OneToOneField(WritingManager, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.acronym})"
