from django.shortcuts import render, reverse
from .functions_create_objects import create_committee, reset_committee
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .functions_read_files import read_file
from .views_my_committee import *
from .views_writing import *


# Create your views here.
def index(request):
    """loads the index page"""
    context = {}
    reset_committee()
    read_file("categories")
    read_file("modes")
    read_file("motions")
    read_file("pp_rubric")
    read_file("part_rubric")
    read_file("reso_rubric")
    create_committee()
    return render(request, 'dartmun/index.html', context)


def get_committee(request):
    """determines the user's committee"""
    if request.user.is_staff:
        chair = Chair.objects.get(user=request.user)
        try:
            cd = CommitteeDirector.objects.get(chair=chair)
            manager = PeopleManager.objects.get(directors=cd)
        except:
            cm = CommitteeManager.objects.get(chair=chair)
            manager = PeopleManager.objects.get(directors=cm)
    else:
        delegation = Delegation.objects.get(user=request.user)
        manager = PeopleManager.objects.get(delegations=delegation)
    return Committee.objects.get(people=manager)


def get_context(request):
    """fills the context dictionary used by multiple pages"""
    committee = get_committee(request)
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
    context = get_context(request)
    return render(request, 'dartmun/mycommittee.html', context)


@staff_member_required
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


@staff_member_required
def tallies(request):
    """loads a transcript of the tallies"""
    context = get_context(request)
    return render(request, 'dartmun/tallies.html', context)


@login_required
def pospapers(request):
    """loads the position papers page"""
    context = get_context(request)
    return render(request, 'dartmun/pospapers.html', context)


@staff_member_required
def delegation_papers(request, id):
    """gets a delegation's position papers"""
    context = get_context(request)
    delegation = Delegation.objects.get(pk=id)
    context['delegation'] = delegation
    category = TallyCategory.objects.get(acronym="PP")
    context['papers'] = TallyScore.objects.filter(delegation=delegation, category=category)
    return render(request, 'dartmun/pospapers.html', context)


@staff_member_required
def update_paper(request, id):
    """updates a paper's score"""
    paper = TallyScore.objects.get(pk=int(id))
    old_score = paper.score
    if request.POST.get("late"):
        paper.score = 0
        paper.rubric.total_score = 0
        paper.save()
    else:
        for criterion in paper.rubric.criterion_scores.all():
            score = request.POST.get(f"criterion{criterion.id}")
            if score:
                criterion.update_score(float(score))
            comments = request.POST.get("comments")
            if comments:
                paper.comments = comments
                paper.save()
        paper.set_rubric_score()
    committee = get_committee(request)
    committee.grades.update_tally(paper, old_score)
    return HttpResponseRedirect(reverse('delegation_papers', kwargs={"id": paper.delegation.id}))


@login_required
def resos(request):
    """loads the writings page"""
    context = get_context(request)
    context['reso_rubric'] = Rubric.objects.get(title="Resolution Rubric")
    context['part_rubric'] = Rubric.objects.get(title="Participation Rubric")
    context['part_tallies'] = get_category_tallies("P", "UNEP")
    return render(request, 'dartmun/resos.html', context)


