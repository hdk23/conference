from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .views import get_committee
from .models import *


@staff_member_required(login_url='/admin/login/')
def add_wp(request):
    """adds a working paper"""
    topic = Topic.objects.get(pk=int(request.POST.get("topic")))
    sponsor_ids = request.POST.getlist('sponsors')
    signatory_ids = request.POST.getlist('signatories')
    not_enough = len(sponsor_ids) + len(signatory_ids) - int(request.POST.get("min_count"))
    if not_enough >= 0:
        topic.add_wp(sponsor_ids, signatory_ids)
    return HttpResponseRedirect(reverse('resos'))


@staff_member_required(login_url='/admin/login/')
def remove_wp(request, id):
    """removes a working paper"""
    WorkingPaper.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('resos'))


@staff_member_required(login_url='/admin/login/')
def add_reso(request):
    """add resolution entry"""
    topic = Topic.objects.get(pk=int(request.POST.get("topic")))
    sponsor_ids = request.POST.getlist('sponsors')
    signatory_ids = request.POST.getlist('signatories')
    scores = request.POST.getlist('score')
    reso = topic.add_reso(sponsor_ids, signatory_ids)

    rubric = Rubric.objects.get(title="Resolution Rubric")
    rubric_entry = RubricEntry(rubric=rubric, topic=topic)
    rubric_entry.save()
    rubric_entry.add_scores(scores)
    committee = get_committee(request)
    committee.grades.add_reso_grades(reso, topic, rubric_entry)
    return HttpResponseRedirect(reverse('resos'))


@staff_member_required(login_url='/admin/login/')
def remove_reso(request, id):
    """removes a resolution and the corresponding tally entries"""
    Resolution.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('resos'))


def get_category_tallies(category_acronym, committee_acronym):
    """helper method that gets a category's tallies"""
    category = TallyCategory.objects.get(acronym=category_acronym)
    committee = Committee.objects.get(acronym=committee_acronym)
    return committee.grades.tallies.filter(category=category).order_by('delegation__country')


@staff_member_required(login_url='/admin/login/')
def update_participation(request):
    part_tallies = get_category_tallies("P", "UNEP")
    for tally in part_tallies:
        old_score = tally.score
        for criterion in tally.rubric.criterion_scores.all():
            if request.POST.get(f"criterion{criterion.id}"):
                new_score = float(request.POST.get(f"criterion{criterion.id}"))
                tally.rubric.replace_criterion(criterion, new_score)
        tally.set_rubric_score()
        print("update part", tally.score)
        committee = Committee.objects.get(acronym="UNEP")
        committee.grades.update_tally(tally, old_score)
    return HttpResponseRedirect(reverse('resos'))
