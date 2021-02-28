from django.db import models
from .models_people import Delegation
from datetime import datetime, timedelta
from django.utils import timezone


class Topic(models.Model):
    topic = models.CharField(max_length=128)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Topic {self.number}: {self.topic}"


class Motion(models.Model):
    """Motion class for motions raised by delegates in Model UN"""
    motion = models.CharField(max_length=64)
    choices = [('simple', 'simple majority'), ('2/3', '2/3 majority')]
    vote_type = models.CharField(choices=choices, max_length=16, default='simple')
    speeches = models.BooleanField(default=False)
    duration = models.BooleanField(default=False)
    speaking_time = models.BooleanField(default=False)
    topic = models.BooleanField(default=False)
    purpose = models.BooleanField(default=False)

    def __str__(self):
        return f"Motion to {self.motion}"


class DebateMode(models.Model):
    mode = models.CharField(max_length=64)
    acronym = models.CharField(max_length=8)
    speeches = models.BooleanField(default=False)
    yielding = models.BooleanField(default=False)
    duration = models.BooleanField(default=False)
    speaking_time = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mode}"


class MotionEntry(models.Model):
    motion = models.ForeignKey(Motion, on_delete=models.CASCADE)
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)
    priority = models.FloatField(default=0)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    speaking_time = models.PositiveSmallIntegerField(blank=True, null=True)
    topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=128, blank=True, null=True)

    def passes(self, votes_for: int, votes_against: int) -> bool:
        """calculates whether a motion passes by a simple or 2/3 majority"""
        if self.motion.vote_type == 'simple':
            return votes_for > votes_against
        else:
            return votes_for >= votes_against * 2

    def calc_motion_score(self, votes_for: int, votes_against=0) -> int:
        """
        calculates the motion's score based on whether the motion passed
        the number of votes for, and the motion's vote type
        """
        if self.passes(votes_for, votes_against):
            if self.motion.vote_type == '2/3':
                score = votes_for * 3
            else:
                score = votes_for * 2
        else:
            score = votes_for
        return score

    def __str__(self):
        if self.motion.motion == "Move into a Moderated Caucus":
            return f"{self.delegation.country.name} - Mod {self.duration}/{self.speaking_time} to {self.purpose.lower()}"
        elif self.motion.motion == "Move into an Unmoderated Caucus":
            return f"{self.delegation.country.name} - Unmod {self.duration}"
        elif self.motion.motion == "Set a Working Agenda":
            return f"{self.delegation.country.name} - Set Agenda to Topic {self.topic.number}"
        return f"{self.delegation.country.name} - {self.motion}"


class SpeechEntry(models.Model):
    delegation = models.OneToOneField(Delegation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.delegation} on the Speaker's List"

