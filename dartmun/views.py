from django.shortcuts import render, reverse
from .functions_create_objects import create_committee, reset_committee
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .functions_read_files import read_file
from .views_my_committee import *
import time
committee = Committee.objects.get(acronym="UNEP")


# Create your views here.
def index(request):
    """loads the index page"""
    context = {}
    reset_committee()
    read_file("groups")
    read_file("categories")
    read_file("modes")
    read_file("motions")
    pp_rubric = Rubric(title="Position Paper Rubric", tally_category=TallyCategory.objects.get(acronym="PP"))
    pp_rubric.save()
    read_file("pp_rubric")
    create_committee()
    return render(request, 'dartmun/index.html', context)


def get_context():
    committee = Committee.objects.get(acronym="UNEP")
    committee.parli_pro.caucus_over()
    context = {'committee': committee, 'delegations': committee.people.sorted_present_delegations(),
               'all_delegations': committee.people.sorted_all_delegations(), 'modes': DebateMode.objects.all(),
               'motions': Motion.objects.all(), 'open': Motion.objects.get(motion="Open Debate"),
               'set': Motion.objects.get(motion="Set a Working Agenda")
               }
    return context


@login_required
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
    context = get_context()
    context['tally_categories'] = TallyCategory.objects.all()
    if context['committee'].grades.need_update:
        context['committee'].grades.calc_grades()
    context['score_managers'] = context['committee'].grades.score_managers.order_by('delegation__country').order_by('-score')
    return render(request, 'dartmun/grades.html', context)


@staff_member_required
def tallies(request):
    """loads a transcript of the tallies"""
    context = get_context()
    return render(request, 'dartmun/tallies.html', context)


@login_required
def pospapers(request):
    """loads the position papers page"""
    context = get_context()
    return render(request, 'dartmun/pospapers.html', context)

@staff_member_required
def delegation_papers(request, id):
    """gets a delegation's position papers"""
    context = get_context()
    delegation = Delegation.objects.get(pk=id)
    context['delegation'] = delegation
    category = TallyCategory.objects.get(acronym="PP")
    context['papers'] = TallyScore.objects.filter(delegation=delegation, category=category)
    return render(request, 'dartmun/pospapers.html', context)