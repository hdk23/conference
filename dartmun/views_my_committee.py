from django.shortcuts import render, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .views_context import *


@staff_member_required(login_url='/admin/login/')
def add_speech_entry(request):
    """adds an entry to the speaker's list"""
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    committee = get_committee(request)
    committee.parli_pro.add_speaker(delegation)
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def remove_speech_entry(request, id):
    """removes an entry from the speaker's list"""
    committee = get_committee(request)
    committee.parli_pro.remove_speaker(id)
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def add_tally(request):
    """adds tally for the delegation"""
    committee = get_committee(request)
    delegation_id = int(request.POST.get("delegation"))
    delegation = Delegation.objects.get(pk=delegation_id)
    score = int(request.POST.get("score"))
    comments = request.POST.get("comments")
    time = request.POST.get("time")
    category = TallyCategory.objects.get(acronym="S")
    tally = TallyScore(scorer=Chair.objects.get(user=request.user), delegation=delegation, category=category,
                       score=score)
    if comments:
        tally.comments = comments
    if time:
        tally.time = time
    tally.save()
    committee.grades.add_tally(tally)
    committee.parli_pro.after_tally(delegation)
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def remove_tally(request, id):
    """removes a tally from a delegation's record"""
    committee = get_committee(request)
    tally = TallyScore.objects.get(pk=id)
    committee.grades.remove_tally(tally)
    return HttpResponseRedirect(reverse('tallies'))


def create_motion_tally(request, motion_entry, score):
    scorer = Chair.objects.get(user=request.user)
    category = TallyCategory.objects.get(acronym="M")
    motion_tally = TallyScore(scorer=scorer, delegation=motion_entry.delegation, category=category, score=score, motion=motion_entry.motion)
    motion_tally.save()
    return motion_tally


@staff_member_required(login_url='/admin/login/')
def add_motion_entry(request):
    committee = get_committee(request)
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
    if motion.motion == "Introduce a Working Paper":
        committee.writing.set_wp(int(request.POST.get("wp")))
    elif motion.motion == "Introduce a Resolution":
        committee.writing.set_reso(int(request.POST.get("reso")))
    elif motion.motion == "Introduce an Amendment":
        committee.writing.set_amend(int(request.POST.get("amend")))
    elif motion.motion == "Recess":
        pass
    elif motion.motion == "Adjourn":
        pass
    motion_entry.save()
    if request.POST.get("discretion") or "Introduce" in motion.motion:
        present = committee.people.delegations.filter(present=True).count()
        score = motion_entry.calc_motion_score(present)
        motion_tally = create_motion_tally(request, motion_entry, score)
        committee.grades.add_tally(motion_tally)
        committee.parli_pro.handle_vote(motion_entry)
    else:
        committee.parli_pro.motion_list.add(motion_entry)
    committee.parli_pro.save()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def remove_motion_entry(request, id):
    """removes an entry from the motion list"""
    MotionEntry.objects.get(pk=id).delete()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def vote_motion(request):
    """votes on the motion"""
    committee = get_committee(request)
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


@staff_member_required(login_url='/admin/login/')
def update_attendance(request):
    """updates committee attendance"""
    committee = get_committee(request)
    for delegation in committee.people.delegations.all():
        attendance = request.POST.get(f"attendance{delegation.id}")
        delegation.update_attendance(attendance)
    committee.people.count_present()
    committee.people.calc_votes()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def set_mod_speaker(request, order):
    """sets the delegate that raised the motion as either the first or last speaker"""
    committee = get_committee(request)
    committee.parli_pro.caucus.set_mod_speaker(order)
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def ssl(request):
    """starts a secondary speaker's list (SSL) for the committee"""
    committee = get_committee(request)
    committee.parli_pro.start_ssl()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def add_amendment(request):
    amend_type = request.POST.get("type")
    clause = int(request.POST.get("clause"))
    friendly = request.POST.get("friendly")
    score = int(request.POST.get("score"))
    original = request.POST.get("original")
    new = request.POST.get("new")
    sponsor = Delegation.objects.get(pk=int(request.POST.get("sponsor")))
    signatory_ids = request.POST.getlist('signatories')
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def reset_wp(request):
    committee = get_committee(request)
    committee.writing.reset_wp()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def reset_reso(request):
    committee = get_committee(request)
    committee.writing.reset_reso()
    return HttpResponseRedirect(reverse('my_committee'))


@staff_member_required(login_url='/admin/login/')
def reset_amend(request):
    committee = get_committee(request)
    committee.writing.reset_amend()
    return HttpResponseRedirect(reverse('my_committee'))