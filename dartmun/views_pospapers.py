from .models import *
from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .views_context import get_context, get_committee


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
        paper.mark_late()
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