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


@staff_member_required
def add_speech_entry(request):
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    committee = Committee.objects.first()
    try:
        speech_entry = SpeechEntry(delegation=delegation)
        speech_entry.save()
        committee.parli_pro.speaker_list.add(speech_entry)
        committee.save()
    except:
        print("The delegate is already on the speaker's list.")
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def remove_speech_entry(request, id):
    SpeechEntry.objects.get(pk=int(id)).delete()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def add_tally(request):
    """adds tally for the delegation"""
    speech_entry_id = int(request.POST.get("delegation"))
    speech_entry = SpeechEntry.objects.get(pk=speech_entry_id)
    delegation_id = speech_entry.delegation.id
    delegation = Delegation.objects.get(pk=delegation_id)
    score = int(request.POST.get("score"))
    comments = request.POST.get("comments")
    time = request.POST.get("time")
    category = TallyCategory.objects.get(acronym="S")
    tally = TallyScore(scorer=Chair.objects.get(user=request.user), delegation=delegation, category=category, score=score, comments=comments)
    if time:
        tally.time = time
    tally.save()
    committee = Committee.objects.get(acronym="UNEP")
    committee.grades.add_tally(tally)
    return remove_speech_entry(request, speech_entry_id)


@staff_member_required
def remove_tally(request, id):
    tally = TallyScore.objects.get(pk=id)
    score_manager = ScoreManager.objects.get(delegation=tally.delegation)
    committee = Committee.objects.first()
    committee.grades.remove_tally(tally)
    for tally_category in score_manager.tally_category_scores.all():
        print(tally_category.tallies.all())
        if tally in tally_category.tallies.all():
            tally_category.remove_tally(tally)
            break
    return HttpResponseRedirect(reverse('tallies'))


@staff_member_required
def add_motion_entry(request):
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    motion_id = int(request.POST.get("motion"))
    motion = Motion.objects.get(pk=motion_id)
    motion_entry = MotionEntry(motion=motion, delegation=delegation)
    motion_entry.save()
    if motion.duration:
        motion_entry.duration = int(request.POST.get("duration"))
    if motion.speaking_time:
        motion_entry.speaking_time = int(request.POST.get("speaking_time"))
    if motion.purpose:
        motion_entry.purpose = request.POST.get("purpose")
    motion_entry.save()
    committee = Committee.objects.first()
    committee.parli_pro.motion_list.add(motion_entry)
    committee.save()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def remove_motion_entry(request, id):
    MotionEntry.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('my_committee'))


def calc_motion_score(passes, vote_type, votes_for):
    if passes:
        if vote_type == '2/3':
            score = votes_for * 3
        else:
            score = votes_for * 2
    else:
        score = votes_for
    return score


@staff_member_required
def vote_motion(request):
    motion_entry_id = int(request.POST.get("motion-entry"))
    motion_entry = MotionEntry.objects.get(pk=motion_entry_id)
    votes_for = int(request.POST.get("votes-for"))
    votes_against = int(request.POST.get("votes-against"))
    passes = motion_entry.passes(votes_for, votes_against)
    score = calc_motion_score(passes, motion_entry.motion.vote_type, votes_for)
    scorer = Chair.objects.get(user=request.user)
    category = TallyCategory.objects.get(acronym="M")
    motion_tally = TallyScore(scorer=scorer, delegation=motion_entry.delegation, category=category, score=score)
    motion_tally.save()
    committee = Committee.objects.first()
    if passes and motion_entry.motion.motion == "Move into a Moderated Caucus":
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Mod")
        committee.parli_pro.current_st = motion_entry.speaking_time
        committee.parli_pro.caucus_duration = motion_entry.duration
        committee.parli_pro.remaining_speeches = motion_entry.duration * 60 / motion_entry.speaking_time
        committee.parli_pro.save()
    elif passes and motion_entry.motion.motion == "Move into an Unmoderated Caucus":
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Unmod")
        committee.parli_pro.caucus_duration = motion_entry.duration
        committee.parli_pro.save()
    committee.grades.add_tally(motion_tally)
    committee.grades.save()
    motion_entry.delete()
    return HttpResponseRedirect(reverse('my_committee'))


