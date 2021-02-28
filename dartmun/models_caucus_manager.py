from datetime import datetime, timedelta
from django.db import models
from .models_people import Delegation
from .models_parli_pro import MotionEntry, DebateMode


class CaucusManager(models.Model):
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

    def set_unmod(self, motion_entry: MotionEntry):
        """sets the values for an unmoderated caucus"""
        self.caucus_duration = motion_entry.duration
        self.caucus_until = (datetime.now() + timedelta(minutes=self.caucus_duration)).time()
        self.save()

    def decrement_speech_count(self):
        """decrements the speech count during a moderated caucus"""
        self.remaining_speeches -= 1
        if self.remaining_speeches == 0:
            self.current_mode = DebateMode.objects.get(acronym="Open")
            self.caucus_duration = None
            self.current_st = None
        self.save()

    def caucus_over(self) -> bool:
        """returns whether the unmoderated caucus is over"""
        print(self.caucus_until)
        print(datetime.now().time())
        if self.caucus_until and datetime.now().time() >= self.caucus_until:
            self.caucus_duration = None
            self.caucus_until = None
            self.save()
            return True
        return False

    def __str__(self):
        if self.current_st and self.caucus_duration:
            return f"Mod: {self.caucus_duration}/{self.current_st}"
        elif self.caucus_until:
            return f"Unmod Until {self.caucus_until}"
        else:
            return f"Caucus Manager"
