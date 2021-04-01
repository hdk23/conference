from django.db import models
from .models_writing import *


class WritingManager(models.Model):
    """Writing Manager class to handle working papers and resolutions"""
    current_wp = models.ForeignKey(WorkingPaper, on_delete=models.CASCADE, null=True, blank=True, related_name="current_wp")
    current_reso = models.ForeignKey(Resolution, on_delete=models.CASCADE, null=True, blank=True, related_name="current_reso")
    current_amend = models.ForeignKey(Amendment, on_delete=models.CASCADE, null=True, blank=True, related_name="current_amend")

    def set_wp(self, wp_id):
        """sets the current working paper"""
        self.current_wp = WorkingPaper.objects.get(pk=wp_id)
        self.current_wp.introduced = True
        self.current_wp.save()
        self.current_reso = None
        self.save()

    def reset_wp(self):
        """resets the current working paper"""
        self.current_wp = None
        self.save()

    def set_reso(self, reso_id):
        """sets the current resolution"""
        self.current_reso = Resolution.objects.get(pk=reso_id)
        self.current_reso.introduced = True
        self.current_reso.save()
        self.current_wp = None
        self.save()

    def reset_reso(self):
        """resets the current resolution"""
        self.current_reso = None
        self.save()

    def vote_reso(self, votes_for, votes_against, votes_abstain):
        """votes on the current resolution"""
        self.current_reso.passes(votes_for, votes_against, votes_abstain)
        self.reset_reso()

    def set_amend(self, amend_id):
        """sets the current amendment"""
        self.current_amend = Amendment.objects.get(pk=amend_id)
        self.current_amend.introduced = True
        self.current_amend.save()
        self.save()

    def reset_amend(self):
        """resets the current amend"""
        self.current_amend = None
        self.save()

    def vote_amend(self, votes_for, votes_against, votes_abstain):
        """votes on the current amend"""
        self.current_amend.passes(votes_for, votes_against, votes_abstain)
        self.reset_amend()

    def reset(self):
        self.reset_reso()
        self.reset_wp()
        self.reset_amend()

    def __str__(self):
        if self.current_wp:
            return f"Current WP: {self.current_wp}"
        elif self.current_reso:
            return f"Current Reso: {self.current_reso}"
        elif self.current_amend:
            return f"Current Amend:{self.current_amend}"
        else:
            return f"Writing Manager"
