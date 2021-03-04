from django.db import models
from .models_parli_pro import *
from .models_caucus_manager import CaucusManager


class ParliProManager(models.Model):
    """Parli Pro Manager to manage caucuses, speakers, and motions"""
    open = models.BooleanField(default=False)
    default_st = models.PositiveSmallIntegerField(default=120)
    caucus = models.ForeignKey(CaucusManager, blank=True, null=True, on_delete=models.CASCADE)
    current_topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.CASCADE)
    current_mode = models.ForeignKey(DebateMode, blank=True, null=True, on_delete=models.CASCADE)
    speaker_list = models.ManyToManyField(SpeechEntry, blank=True)
    motion_list = models.ManyToManyField(MotionEntry, blank=True)

    def start_ssl(self):
        """starts a secondary speaker's list in the committee"""
        self.current_mode = DebateMode.objects.get(acronym="SSL")
        self.save()

    def add_speaker(self, delegation: Delegation):
        """adds speaker to the speaker list"""
        if self.current_mode.acronym != "PSL":
            self.current_mode = DebateMode.objects.get(acronym="SSL")
            self.save()
        try:
            speech_entry = SpeechEntry(delegation=delegation)
            speech_entry.save()
            self.speaker_list.add(speech_entry)
            self.save()
        except:
            print("The delegate is already on the speaker's list.")

    def remove_speaker(self, id):
        """removes speaker from the speaker list"""
        SpeechEntry.objects.get(pk=int(id)).delete()
        if self.speaker_list.count() == 0:
            self.current_mode = DebateMode.objects.get(acronym="Open")
            self.save()

    def handle_vote(self, motion_entry: MotionEntry):
        """updates the parli pro manager based on the motion entry"""
        if motion_entry.motion.motion == "Move into a Moderated Caucus":
            self.current_mode = DebateMode.objects.get(acronym="Mod")
            self.caucus.set_mod(motion_entry)
            self.save()
        elif motion_entry.motion.motion == "Move into an Unmoderated Caucus":
            self.current_mode = DebateMode.objects.get(acronym="Unmod")
            self.caucus.set_unmod(motion_entry)
            self.save()
        elif motion_entry.motion.motion == "Set a Working Agenda":
            self.current_mode = DebateMode.objects.get(acronym="Open")
            self.current_topic = motion_entry.topic
            self.save()
        elif motion_entry.motion.motion == "Set the Speaking Time":
            self.caucus.default_st = motion_entry.speaking_time
            self.save()
        elif motion_entry.motion.motion == "Open Debate":
            self.current_mode = DebateMode.objects.get(acronym="PSL")
            self.open = True
            self.save()
        self.save()
        motion_entry.delete()

    def after_tally(self, delegation: Delegation):
        """updates the parli pro manager after adding the tally"""
        if self.current_mode.acronym == "SSL" or self.current_mode.acronym == "PSL":
            speech_entry = SpeechEntry.objects.get(delegation=delegation)
            self.remove_speaker(speech_entry.id)
            if not self.speaker_list.count():
                self.current_mode = DebateMode.objects.get(acronym="Open")
        elif self.current_mode.acronym == "Mod":
            self.caucus.decrement_speech_count()
            if self.caucus.end_mod():
                self.current_mode = DebateMode.objects.get(acronym="Open")
        self.save()

    def caucus_over(self):
        """determines whether the caucus is over based on the time until"""
        if self.current_mode and self.current_mode.acronym == "Unmod" and self.caucus.caucus_over():
            self.current_mode = DebateMode.objects.get(acronym="Open")
        self.save()

    def __str__(self):
        if self.current_topic and self.current_mode.acronym:
            return f"Topic {self.current_topic.number}, {self.current_mode.acronym}"
        return f"Parli Pro Manager"
