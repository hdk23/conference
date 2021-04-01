from django.db import models


class Session(models.Model):
    """Session model to track conference sessions"""
    number = models.IntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    counts = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.number} from {self.start_time} to {self.end_time}"
