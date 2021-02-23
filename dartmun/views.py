from django.shortcuts import render, reverse
from .functions_create_objects import create_committee, reset_committee
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .functions_read_files import read_file
from .models import *
from .views_my_committee import *


# Create your views here.
def index(request):
    """loads the index page"""
    context = {}
    reset_committee()
    read_file("groups")
    read_file("categories")
    read_file("modes")
    read_file("motions")
    create_committee()
    return render(request, 'dartmun/index.html', context)


def get_context():
    context = {}
    context['committee'] = Committee.objects.first()
    context['delegations'] = context['committee'].people.delegations.order_by('country')
    context['modes'] = DebateMode.objects.all()
    context['motions'] = Motion.objects.all()
    context['open'] = Motion.objects.get(motion="Open Debate")
    context['set'] = Motion.objects.get(motion="Set a Working Agenda")
    return context


def my_committee(request):
    """loads the my committee page"""
    context = get_context()
    committee = Committee.objects.first()
    committee.people.calc_votes()
    return render(request, 'dartmun/mycommittee.html', context)


@staff_member_required
def grades(request):
    """
    loads the page that displays all delegations' grades
    recalculates delegates' scores each time
    """
    context = get_context()
    context['tally_categories'] = TallyCategory.objects.all()
    committee = context['committee']
    if committee.grades.need_update:
        context['committee'].grades.calc_grades()
    context['score_managers'] = context['committee'].grades.score_managers.order_by('-score')
    return render(request, 'dartmun/grades.html', context)


@staff_member_required
def tallies(request):
    """loads a transcript of the tallies"""
    context = get_context()
    return render(request, 'dartmun/tallies.html', context)





