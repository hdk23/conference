from django.shortcuts import render, reverse
from .functions_create_objects import create_committee, reset_committee
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .functions_read_files import read_file
from .views_my_committee import *
from .views_admin import *
from .views_context import *
from .views_pospapers import *
from .views_writing import *


# Create your views here.
def index(request):
    """loads the index page"""
    context = {}
    # reset_committee()
    # read_file("categories")
    # read_file("modes")
    # read_file("motions")
    # read_file("pp_rubric")
    # read_file("part_rubric")
    # read_file("reso_rubric")
    # create_committee()
    return render(request, 'dartmun/index.html', context)


@login_required(login_url='/registration/login/')
def my_committee(request):
    """loads the my committee page"""
    context = get_context(request)
    return render(request, 'dartmun/mycommittee.html', context)


@staff_member_required(login_url='/admin/login/')
def grades(request):
    """
    loads the page that displays all delegations' grades
    recalculates delegates' scores each time
    """
    context = get_context(request)
    context['tally_categories'] = TallyCategory.objects.all()
    if context['committee'].grades.need_update:
        context['committee'].grades.calc_grades()
    context['score_managers'] = context['committee'].grades.score_managers.order_by('delegation__country').order_by('-score')
    return render(request, 'dartmun/grades.html', context)


@staff_member_required(login_url='/admin/login/')
def tallies(request):
    """loads a transcript of the tallies"""
    context = get_context(request)
    return render(request, 'dartmun/tallies.html', context)


@login_required(login_url='/registration/login/')
def resos(request):
    """loads the writings page"""
    context = get_context(request)
    context['reso_rubric'] = Rubric.objects.get(title="Resolution Rubric")
    context['part_rubric'] = Rubric.objects.get(title="Participation Rubric")
    context['part_tallies'] = get_category_tallies("P", "UNEP")
    return render(request, 'dartmun/resos.html', context)


@staff_member_required(login_url='/admin/login/')
def admin(request):
    """admin page to add/remove delegations"""
    context = get_context(request)
    context['countries'] = CountryField()
    taken_countries = []
    committee = get_committee(request)
    for delegation in committee.people.delegations.all():
        taken_countries.append(delegation.country)
    context['taken_countries'] = taken_countries
    return render(request, 'dartmun/admin.html', context)
