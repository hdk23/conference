from django.shortcuts import render, reverse
from .functions_create_objects import create_committee, reset_committee
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .functions_read_files import read_file
from .models import *


# Create your views here.
def index(request):
    """loads the index page"""
    context = {}
    reset_committee()
    read_file("groups")
    read_file("categories")
    create_committee()
    return render(request, 'dartmun/index.html', context)


def get_context():
    context = {}
    context['committee'] = Committee.objects.first()
    context['delegations'] = context['committee'].delegations.order_by('country')
    return context


def my_committee(request):
    """loads the my committee page"""
    context = get_context()
    return render(request, 'dartmun/mycommittee.html', context)


@staff_member_required
def grades(request):
    """
    loads the page that displays all delegations' grades
    recalculates delegates' scores each time
    """
    pass


@staff_member_required
def tallies(request):
    """loads a transcript of the tallies"""
    context = get_context()
    tallies = []
    for delegation in context['committee'].delegations.all():
        for tally_category in delegation.tally_category_scores.all():
            for tally in tally_category.tallies.all():
                tallies.append(tally)
    tallies.sort(key=lambda tally: tally.timestamp)
    context['tallies'] = tallies
    return render(request, 'dartmun/tallies.html', context)


@staff_member_required
def add_tally(request):
    """adds tally for the delegation"""
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    score = int(request.POST.get("score"))
    comments = request.POST.get("comments")
    time = request.POST.get("time")
    category = TallyCategory.objects.get(acronym="S")
    tally = TallyScore(scorer=Chair.objects.get(user=request.user), score=score, comments=comments)
    if time:
        tally.time = time
    tally.save()
    category_score = delegation.tally_category_scores.get(category=category)
    category_score.add_tally(tally)
    category_score.save()
    return HttpResponseRedirect(reverse('my_committee'))
