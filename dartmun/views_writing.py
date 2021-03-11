from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *


@staff_member_required
def add_wp(request):
    """adds a working paper"""
    topic = Topic.objects.get(pk=int(request.POST.get("topic")))
    sponsor_ids = request.POST.getlist('sponsors')
    signatory_ids = request.POST.getlist('signatories')
    topic.add_wp(sponsor_ids, signatory_ids)
    return HttpResponseRedirect(reverse('resos'))


@staff_member_required
def remove_wp(request, id):
    """removes a working paper"""
    WorkingPaper.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('resos'))


@staff_member_required
def add_reso(request):
    topic = Topic.objects.get(pk=int(request.POST.get("topic")))
    sponsor_ids = request.POST.getlist('sponsors')
    signatory_ids = request.POST.getlist('signatories')
    scores = request.POST.getlist('score')
    reso = topic.add_reso(sponsor_ids, signatory_ids)

    rubric = Rubric.objects.get(title="Resolution Rubric")
    rubric_entry = RubricEntry(rubric=rubric, topic=topic)
    rubric_entry.save()
    rubric_entry.add_scores(scores)
    committee = Committee.objects.get(acronym="UNEP")
    committee.grades.add_reso_grades(reso, topic, rubric_entry)

    return HttpResponseRedirect(reverse('resos'))