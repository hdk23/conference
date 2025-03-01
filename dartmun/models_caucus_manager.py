from datetime import datetime, timedelta
from django.db import models
from .models_people import Delegation
from .models_parli_pro import MotionEntry, DebateMode


class CaucusManager(models.Model):
    """Caucus Manager to manage caucus functionalities (unmod/mod)"""
    caucus_duration = models.PositiveSmallIntegerField(blank=True, null=True)
    caucus_until = models.TimeField(blank=True, null=True)
    current_st = models.PositiveSmallIntegerField(blank=True, null=True)
    remaining_speeches = models.PositiveSmallIntegerField(blank=True, null=True)
    raised_by = models.ForeignKey(Delegation, blank=True, null=True, on_delete=models.CASCADE)
    last = models.BooleanField(blank=True, null=True)
    spoke = models.BooleanField(blank=True, null=True)  # used to indicate whether the first speaker spoke

    def set_mod(self, motion_entry: MotionEntry):
        """sets the values for a moderated caucus"""
        self.current_st = motion_entry.speaking_time
        self.caucus_duration = motion_entry.duration
        self.remaining_speeches = motion_entry.duration * 60 / motion_entry.speaking_time
        self.raised_by = motion_entry.delegation
        self.save()

    def set_mod_speaker(self, order):
        """sets the delegation that raised the motion as either the first or last speaker"""
        if order == "first":
            self.last = False
            self.spoke = False
        else:
            self.last = True
        self.save()

    def set_unmod(self, motion_entry: MotionEntry):
        """sets the values for an unmoderated caucus"""
        self.caucus_duration = motion_entry.duration
        self.caucus_until = (datetime.now() + timedelta(minutes=self.caucus_duration)).time()
        self.save()

    def end_mod(self) -> bool:
        """ends the moderated caucus if there are no speakers left"""
        print(self.remaining_speeches)
        if self.remaining_speeches == 0:
            self.last = None
            self.spoke = None
            self.save()
            return True
        return False

    def decrement_speech_count(self):
        """decrements the speech count during a moderated caucus"""
        self.remaining_speeches -= 1
        if self.remaining_speeches == 0:
            self.caucus_duration = None
            self.current_st = None

        if self.spoke is False:
            self.spoke = True
        self.save()

    def caucus_over(self) -> bool:
        """returns whether the unmoderated caucus is over"""
        print(datetime.now().time())
        print(self.caucus_until)
        if self.caucus_until and datetime.now().time() >= self.caucus_until:
            self.caucus_duration = None
            self.caucus_until = None
            self.save()
            return True
        return False

    def reset(self):
        self.caucus_duration = None
        self.caucus_until = None
        self.current_st = None
        self.remaining_speeches = None
        self.raised_by = None
        self.last = None
        self.spoke = None
        self.save()

    def __str__(self):
        if self.current_st and self.caucus_duration:
            return f"Moderated Caucus: {self.caucus_duration}/{self.current_st}"
        elif self.caucus_until:
            return f"Unmoderated Caucus Until {self.caucus_until}"
        else:
            return f"Caucus Manager"
