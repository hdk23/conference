from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class Chair(models.Model):
    """
    Chair class that represents committee directors (CDs) and committee managers (CMs)
    Separate classes for CDs and CMs
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(default=2024, null=True)
    major = models.CharField(max_length=64, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Chair {self.user.get_full_name()}"


class CommitteeDirector(models.Model):
    """CD class"""
    chair = models.OneToOneField(Chair, on_delete=models.CASCADE)

    def __str__(self):
        return f"CD {self.chair.user.get_full_name()}"


class CommitteeManager(models.Model):
    """CM class"""
    chair = models.OneToOneField(Chair, on_delete=models.CASCADE)

    def __str__(self):
        return f"CM {self.chair.user.get_full_name()}"


class Delegate(models.Model):
    """
    Delegate class that represents a delegate of a delegation
    Delegate class implemented separated from Delegation class to leave option for double delegation
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Delegate {self.user.get_full_name()}"


class Delegation(models.Model):
    """
    Delegation class that represents a country in a committee
    Assumes that delegates of a delegation are scored together
    Tallies track a delegation's position paper, speech, participation, etc. scores
    Uses the variables present and voting to indicate whether a delegate is present, present & voting, or absent
    """
    country = CountryField()
    delegates = models.ManyToManyField(Delegate)
    present = models.BooleanField(null=True)
    voting = models.BooleanField(null=True)

    def update_attendance(self, attendance: str):
        """
        updates the delegate's attendance status
        P: Present, PV: Present and Voting, A: Absent
        """
        if attendance[0] == "P":
            self.present = True
            self.voting = (attendance == "PV")
            self.save()
        else:
            self.present = False
            self.voting = False
            self.save()

    def get_delegate_names(self):
        names = ""
        for delegate in self.delegates.all():
            names += f"{delegate.user.get_full_name()}, "
        return names[:-2]

    def __str__(self):
        return f"Delegation of {self.country.name}"
        # if self.voting:
        #     return f"Delegation of {self.country.name}: Present and Voting"
        # elif self.present:
        #     return f"Delegation of {self.country.name}: Present"
        # else:
        #     return f"Delegation of {self.country.name}: Absent"


class Advisor(models.Model):
    """Advisor model for faculty advisors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Advisor {self.user.get_full_name()}"


class School(models.Model):
    name = models.CharField(max_length=64)
    advisors = models.ManyToManyField(Advisor)
    delegations = models.ManyToManyField(Delegation)

    def __str__(self):
        return self.name
