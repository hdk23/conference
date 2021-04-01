from .models import *
from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .views_context import get_context, get_committee


@staff_member_required(login_url='/admin/login/')
def manage_delegation(request, id, committee_acronym=None):
    context = get_context(request, committee_acronym)
    delegation = Delegation.objects.get(pk=id)
    context['delegation'] = delegation
    context['scores'] = ScoreManager.objects.get(delegation=delegation)
    category = TallyCategory.objects.get(acronym="PP")
    context['papers'] = TallyScore.objects.filter(delegation=delegation, category=category)
    category = TallyCategory.objects.get(acronym="S")
    context['speeches'] = TallyScore.objects.filter(delegation=delegation, category=category)
    category = TallyCategory.objects.get(acronym="P")
    context['participation'] = TallyScore.objects.get(delegation=delegation, category=category)
    category = TallyCategory.objects.get(acronym="M")
    context['motions'] = TallyScore.objects.filter(delegation=delegation, category=category)
    return render(request, 'dartmun/admin.html', context)


@staff_member_required(login_url='/admin/login/')
def add_delegation(request, committee_acronym=None):
    """adds a delegation via the site admin page"""
    committee = get_committee(request, committee_acronym)
    country = request.POST.get("country")
    inputs = ["first", "last", "email"]
    responses = []
    for form_input in inputs:
        responses.append(request.POST.get(form_input))

    if committee.people.double_delegation:
        for form_input in inputs:
            responses.append(request.POST.get(f"{form_input}2"))
    responses.append(committee.acronym)
    delegation = committee.people.add_delegation(country, responses)
    committee.initialize_delegation(delegation)
    return HttpResponseRedirect(reverse('manage_delegation', kwargs={"id": delegation.id}))


@staff_member_required(login_url='/admin/login/')
def remove_delegation(request, id):
    """removes a delegation via the admin page"""
    Delegation.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('admin'))


@login_required
def password_change_done(request):
    return HttpResponseRedirect(reverse('admin'))
