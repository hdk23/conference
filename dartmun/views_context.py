from .models import *


def get_manager(request):
    """finds the people manager with the chair"""
    chair = Chair.objects.get(user=request.user)
    if len(CommitteeDirector.objects.filter(chair=chair)):
        cd = CommitteeDirector.objects.get(chair=chair)
        manager = PeopleManager.objects.get(directors=cd)
    else:
        cm = CommitteeManager.objects.get(chair=chair)
        manager = PeopleManager.objects.get(managers=cm)
    return manager


def get_conference(request):
    """determines the user's conference"""
    if request.user.is_superuser:
        conference = Conference.objects.get(secretariat=Secretariat.objects.get(user=request.user))
    else:
        if request.user.is_staff:
            manager = get_manager(request)
        else:
            delegate = Delegate.objects.get(user=request.user)
            delegation = Delegation.objects.get(delegates=delegate)
            manager = PeopleManager.objects.get(delegations=delegation)
        committee = Committee.objects.get(people=manager)
        organ = Organ.objects.get(committees=committee)
        conference = Conference.objects.get(organs=organ)
    return conference


def get_committee(request, committee_acronym=None):
    """determines the user's committee"""
    if committee_acronym:
        return Committee.objects.get(acronym=committee_acronym)
    if request.user.is_staff:
        manager = get_manager(request)
    else:
        delegate = Delegate.objects.get(user=request.user)
        delegation = Delegation.objects.get(delegates=delegate)
        manager = PeopleManager.objects.get(delegations=delegation)
    return Committee.objects.get(people=manager)


def get_context(request, committee_acronym=None):
    """fills the context dictionary used by multiple pages"""
    committee = get_committee(request, committee_acronym)
    committee.parli_pro.caucus_over()
    context = {'committee': committee, 'delegations': committee.people.sorted_present_delegations(),
               'all_delegations': committee.people.sorted_all_delegations(), 'modes': DebateMode.objects.all(),
               'motions': Motion.objects.all(), 'open': Motion.objects.get(motion="Open Debate"),
               'set': Motion.objects.get(motion="Set a Working Agenda")
               }
    return context
