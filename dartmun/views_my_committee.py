from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *

committee = Committee.objects.first()


@staff_member_required
def add_speech_entry(request):
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    committee.parli_pro.current_mode = DebateMode.objects.get(acronym="SSL")
    committee.parli_pro.save()
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
    if committee.parli_pro.speaker_list.count() == 0:
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Open")
        committee.parli_pro.save()
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
    tally = TallyScore.objects.get(pk=id)
    score_manager = ScoreManager.objects.get(delegation=tally.delegation)
    committee.grades.remove_tally(tally)
    for tally_category in score_manager.tally_category_scores.all():
        print(tally_category.tallies.all())
        if tally in tally_category.tallies.all():
            tally_category.remove_tally(tally)
            break
    return HttpResponseRedirect(reverse('tallies'))


def calc_motion_score(passes, vote_type, votes_for):
    if passes:
        if vote_type == '2/3':
            score = votes_for * 3
        else:
            score = votes_for * 2
    else:
        score = votes_for
    return score


def create_motion_tally(request, motion_entry, score):
    scorer = Chair.objects.get(user=request.user)
    category = TallyCategory.objects.get(acronym="M")
    motion_tally = TallyScore(scorer=scorer, delegation=motion_entry.delegation, category=category, score=score)
    motion_tally.save()
    return motion_tally


def handle_vote(request, committee, motion_entry, score):
    if motion_entry.motion.motion == "Move into a Moderated Caucus":
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Mod")
        committee.parli_pro.current_st = motion_entry.speaking_time
        committee.parli_pro.caucus_duration = motion_entry.duration
        committee.parli_pro.remaining_speeches = motion_entry.duration * 60 / motion_entry.speaking_time
    elif motion_entry.motion.motion == "Move into an Unmoderated Caucus":
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Unmod")
        committee.parli_pro.caucus_duration = motion_entry.duration
    elif motion_entry.motion.motion == "Set a Working Agenda":
        committee.parli_pro.current_topic = motion_entry.topic
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="Open")
    elif motion_entry.motion.motion == "Set the Speaking Time":
        committee.parli_pro.current_st = motion_entry.speaking_time
    elif motion_entry.motion.motion == "Open Debate":
        committee.parli_pro.current_mode = DebateMode.objects.get(acronym="PSL")
        committee.open = True
    committee.parli_pro.save()
    motion_entry.delete()
    motion_tally = create_motion_tally(request, motion_entry, score)
    committee.grades.add_tally(motion_tally)
    committee.grades.save()


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
    if motion.topic:
        topic_id = int(request.POST.get("topic"))
        motion_entry.topic = Topic.objects.get(pk=topic_id)
    motion_entry.save()
    if request.POST.get("discretion"):
        present = committee.people.delegations.filter(present=True).count()
        score = calc_motion_score(True, motion_entry.motion.vote_type, present)
        handle_vote(request, committee, motion_entry, score)

    else:
        committee.parli_pro.motion_list.add(motion_entry)
    committee.parli_pro.save()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def remove_motion_entry(request, id):
    MotionEntry.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def vote_motion(request):
    motion_entry_id = int(request.POST.get("motion-entry"))
    motion_entry = MotionEntry.objects.get(pk=motion_entry_id)
    votes_for = int(request.POST.get("votes-for"))
    votes_against = int(request.POST.get("votes-against"))
    passes = motion_entry.passes(votes_for, votes_against)
    if passes:
        score = calc_motion_score(True, motion_entry.motion.vote_type, votes_for)
        handle_vote(request, committee, motion_entry, score)
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required
def update_attendance(request):
    for delegation in committee.people.delegations.all():
        attendance = request.POST.get(f"attendance{delegation.id}")
        if attendance[0] == "P":
            delegation.present = True
            if attendance == "PV":
                delegation.voting = True
            else:
                delegation.voting = False
        else:
            delegation.present = False
            delegation.voting = False
        delegation.save()
    committee.people.count_present()
    committee.people.calc_votes()
    return HttpResponseRedirect(reverse('my_committee'))