from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Committee)

# models in models_people
admin.site.register(CommitteeDirector)
admin.site.register(CommitteeManager)
admin.site.register(Delegate)
admin.site.register(Delegation)

# models in models_score
admin.site.register(Chair)
admin.site.register(TallyScore)
admin.site.register(TallyCategoryScore)
admin.site.register(ScoreManager)

# manager models
admin.site.register(PeopleManager)
admin.site.register(GradesManager)
admin.site.register(ParliProManager)
admin.site.register(CaucusManager)

# parlipro models
admin.site.register(Motion)
admin.site.register(DebateMode)
admin.site.register(MotionEntry)
admin.site.register(SpeechEntry)
admin.site.register(Topic)

# models in models_tally
admin.site.register(TallyCategory)
admin.site.register(CommitteeTallyCategory)
admin.site.register(TallyGroup)

# rubric models
admin.site.register(Rubric)
admin.site.register(Criterion)
admin.site.register(Descriptor)
admin.site.register(CriterionScore)
admin.site.register(RubricEntry)