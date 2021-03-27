from .models import *
from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .views_context import get_context, get_committee


def delegation_paper_context(context, request, delegation_id=None):
    if delegation_id:
        delegation = Delegation.objects.get(pk=delegation_id)
    else:
        delegate = Delegate.objects.get(user=request.user)
        delegation = Delegation.objects.get(delegates=delegate)
    context['delegation'] = delegation
    category = TallyCategory.objects.get(acronym="PP")
    context['papers'] = TallyScore.objects.filter(delegation=delegation, category=category)
    return context

@login_required
def pospapers(request):
    """loads the position papers page"""
    context = get_context(request)
    if not request.user.is_staff:
        context = delegation_paper_context(context, request)
    return render(request, 'dartmun/pospapers.html', context)


@staff_member_required(login_url='/admin/login/')
def delegation_papers(request, id):
    """gets a delegation's position papers"""
    context = get_context(request)
    if request.user.is_staff:
        context = delegation_paper_context(context, request, id)
    else:
        context = delegation_paper_context(context, request)
    return render(request, 'dartmun/pospapers.html', context)


@staff_member_required(login_url='/admin/login/')
def update_paper(request, id):
    """updates a paper's score"""
    paper = TallyScore.objects.get(pk=int(id))
    paper.scorer = Chair.objects.get(user=request.user)
    paper.save()
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