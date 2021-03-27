from .models import *


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
        delegate = Delegate.objects.get(user=request.user)
        delegation = Delegation.objects.get(delegates=delegate)
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