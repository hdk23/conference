from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *

committee = Committee.objects.get(acronym="UNEP")


@staff_member_required
def add_speech_entry(request):
    """adds an entry to the speaker's list"""
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    committee.parli_pro.add_speaker(delegation)
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def remove_speech_entry(request, id):
    """removes an entry from the speaker's list"""
    committee.parli_pro.remove_speaker(id)
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
    committee.grades.add_tally(tally)
    if committee.parli_pro.speaker_list.count() == 0:
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Open")
    return remove_speech_entry(request, speech_entry_id)


@staff_member_required
def remove_tally(request, id):
    """removes a tally from a delegation's record"""
    tally = TallyScore.objects.get(pk=id)
    committee.grades.remove_tally(tally)
    return HttpResponseRedirect(reverse('tallies'))


def create_motion_tally(request, motion_entry, score):
    scorer = Chair.objects.get(user=request.user)
    category = TallyCategory.objects.get(acronym="M")
    motion_tally = TallyScore(scorer=scorer, delegation=motion_entry.delegation, category=category, score=score)
    motion_tally.save()
    return motion_tally


@staff_member_required
def add_motion_entry(request):
    committee = Committee.objects.get(acronym="UNEP")
    """adds a motion entry to the motion list"""
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
    if motion.topic:
        topic_id = int(request.POST.get("topic"))
        motion_entry.topic = Topic.objects.get(pk=topic_id)
    motion_entry.save()
    if request.POST.get("discretion"):
        present = committee.people.delegations.filter(present=True).count()
        score = motion_entry.calc_motion_score(present)
        motion_tally = create_motion_tally(request, motion_entry, score)
        committee.grades.add_tally(motion_tally)
        committee.grades.save()
        committee.parli_pro.handle_vote(motion_entry)
    else:
        committee.parli_pro.motion_list.add(motion_entry)
    committee.parli_pro.save()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def remove_motion_entry(request, id):
    """removes an entry from the motion list"""
    MotionEntry.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def vote_motion(request):
    """votes on the motion"""
    motion_entry_id = int(request.POST.get("motion-entry"))
    motion_entry = MotionEntry.objects.get(pk=motion_entry_id)
    votes_for = int(request.POST.get("votes-for"))
    votes_against = int(request.POST.get("votes-against"))
    score = motion_entry.calc_motion_score(votes_for, votes_against)
    if motion_entry.passes(votes_for, votes_against):
        committee.parli_pro.handle_vote(motion_entry)
    else:
        motion_entry.delete()
    motion_tally = create_motion_tally(request, motion_entry, score)
    committee.grades.add_tally(motion_tally)
    committee.grades.save()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def update_attendance(request):
    """updates committee attendance"""
    committee = Committee.objects.get(acronym="UNEP")
    for delegation in committee.people.delegations.all():
        attendance = request.POST.get(f"attendance{delegation.id}")
        delegation.update_attendance(attendance)
    committee.people.count_present()
    committee.people.calc_votes()
    print(committee.people.simple_majority)
    print(committee.people.super_majority)
    return HttpResponseRedirect(reverse('my_committee'))
