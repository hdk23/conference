from django.db import models
from .models_people import Delegation


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
            return f"Set the Working Agenda to Topic {self.topic.number}"
        return f"{self.motion} by {self.delegation.country.name}"


class SpeechEntry(models.Model):
    delegation = models.OneToOneField(Delegation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.delegation} on the Speaker's List"


class ParliProManager(models.Model):
    open = models.BooleanField(default=False)
    default_st = models.PositiveSmallIntegerField(default=120)
    current_st = models.PositiveSmallIntegerField(blank=True, null=True)
    caucus_duration = models.PositiveSmallIntegerField(blank=True, null=True)
    remaining_speeches = models.PositiveSmallIntegerField(blank=True, null=True)
    current_mode = models.ForeignKey(DebateMode, blank=True, null=True, on_delete=models.CASCADE)
    current_topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.CASCADE)
    speaker_list = models.ManyToManyField(SpeechEntry)
    motion_list = models.ManyToManyField(MotionEntry)

    def add_speaker(self, delegation: Delegation):
        """adds speaker to the speaker list"""
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
            self.current_st = motion_entry.speaking_time
            self.caucus_duration = motion_entry.duration
            self.remaining_speeches = motion_entry.duration * 60 / motion_entry.speaking_time
        elif motion_entry.motion.motion == "Move into an Unmoderated Caucus":
            self.current_mode = DebateMode.objects.get(acronym="Unmod")
            self.caucus_duration = motion_entry.duration
        elif motion_entry.motion.motion == "Set a Working Agenda":
            self.current_topic = motion_entry.topic
            self.current_mode = DebateMode.objects.get(acronym="Open")
        elif motion_entry.motion.motion == "Set the Speaking Time":
            self.current_st = motion_entry.speaking_time
        elif motion_entry.motion.motion == "Open Debate":
            self.current_mode = DebateMode.objects.get(acronym="PSL")
            self.open = True
        self.save()
        motion_entry.delete()
    
    def __str__(self):
        return f"Parli Pro Manager"
