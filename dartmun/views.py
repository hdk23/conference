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


@login_required()
def my_committee(request):
    """loads the my committee page"""
    committee = Committee.objects.first()

    delegations = committee.delegations.order_by('country')
    context = {"committee": committee, "delegations":delegations}
    return render(request, 'dartmun/mycommittee.html', context)


@staff_member_required()
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
