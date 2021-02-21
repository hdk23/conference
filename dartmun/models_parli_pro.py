from django.db import models
from .models_people import Delegation


class Motion(models.Model):
    """Motion class for motions raised by delegates in Model UN"""
    motion = models.CharField(max_length=64)
    vote_simple = models.BooleanField(default=True)
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

    def __str__(self):
        return f"{self.motion} by {self.delegation}"


class SpeechEntry(models.Model):
    delegation = models.ForeignKey(Delegation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.delegation} on the Speaker's List"


class ParliProManager(models.Model):
    current_mode = models.ForeignKey(DebateMode, on_delete=models.CASCADE)
    speaker_list = models.ManyToManyField(SpeechEntry)
    motion_list = models.ManyToManyField(MotionEntry)

    def __str__(self):
        return f"Parli Pro Manager"
