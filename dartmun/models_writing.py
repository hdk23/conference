from django.db import models
from .models_people import Delegation
from .models_parli_pro import Topic
from .models_rubric import RubricEntry


class WorkingPaper(models.Model):
    """Working Paper model to represent a working paper"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    sponsors = models.ManyToManyField(Delegation, related_name="wp_sponsors")
    signatories = models.ManyToManyField(Delegation, related_name="wp_signatories")
    introduced = models.BooleanField(default=False)

    def __str__(self):
        return f"Topic {self.topic.number} Working Paper by {self.sponsors.all()}"


class Resolution(models.Model):
    """Resolution model to represent a resolution"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    sponsors = models.ManyToManyField(Delegation, related_name="reso_sponsors")
    signatories = models.ManyToManyField(Delegation, related_name="reso_signatories")
    introduced = models.BooleanField(default=False)
    votes_for = models.PositiveSmallIntegerField(null=True)
    votes_against = models.PositiveSmallIntegerField(null=True)
    votes_abstain = models.PositiveSmallIntegerField(null=True)
    passed = models.BooleanField(null=True)
    rubric_entry = models.ForeignKey(RubricEntry, on_delete=models.CASCADE, null=True)

    def passes(self):
        """calculates whether the motion passes"""
        self.passed = self.votes_for > self.votes_against
        self.save()


class WritingManager(models.Model):
    working_papers = models.ManyToManyField(WorkingPaper, related_name="committee_wps")
    resolutions = models.ManyToManyField(Resolution)
    current_wp = models.ForeignKey(WorkingPaper, on_delete=models.CASCADE, null=True, blank=True, related_name="current_wp")
    current_reso = models.ForeignKey(Resolution, on_delete=models.CASCADE, null=True, blank=True, related_name="current_reso")

    def __str__(self):
        if self.current_wp:
            return f"Current WP: {self.current_wp}"
        elif self.current_reso:
            return f"Current Reso: {self.current_reso}"
        else:
            return f"Writing Manager"