from .models_people import *
from django.db import models


class PeopleManager(models.Model):
    """
    PeopleManager class that manages people in the committee
    Also tracks delegation-count related properties
    """
    directors = models.ManyToManyField(CommitteeDirector)
    managers = models.ManyToManyField(CommitteeManager, blank=True)
    delegations = models.ManyToManyField(Delegation)
    double_delegation = models.BooleanField(default=False)
    quorum = models.PositiveSmallIntegerField(blank=True, null=True)
    simple_majority = models.PositiveSmallIntegerField(blank=True, null=True)
    super_majority = models.PositiveSmallIntegerField(blank=True, null=True)
    min_signatory = models.PositiveSmallIntegerField(blank=True, null=True)
    number_present = models.PositiveSmallIntegerField(default=0)

    def sorted_all_delegations(self):
        """returns the list of all delegations sorted by country"""
        return self.delegations.all().order_by('country')

    def sorted_present_delegations(self):
        """
        returns the list of present delegations sorted by country
        returns None if no delegates have been marked present
        """
        if self.number_present:
            return self.delegations.filter(present=True).order_by('country')
        else:
            return None

    def set_quorum(self):
        self.quorum = round(self.delegations.count() / 4)
        self.save()

    def count_present(self):
        """counts the number of delegates present in the committee"""
        self.number_present = self.delegations.filter(present=True).count()
        self.save()
        return self.delegations.filter(present=True).count()

    def calc_votes(self):
        """
        calculates the number of votes needed for a simple majority or a 2/3 majority
        also sets the minimum signatory count as 1/5 of the delegations present
        """
        self.simple_majority = self.number_present // 2 + 1
        self.super_majority = round(self.number_present * 2 / 3)
        self.min_signatory = round(self.number_present / 5)
        self.save()

    @staticmethod
    def add_delegate(committee_acronym: str, delegation: Delegation, first: str, last: str, email: str, number=1):
        """
        adds a delegate to a delegation
        """
        username = f"{committee_acronym.lower()}{delegation.country.name.lower()}{number}".replace(" ", "")
        user = User(username=username, first_name=first, last_name=last, email=email)
        user.save()
        delegate = Delegate(user=user)
        delegate.save()
        delegation.delegates.add(delegate)
        delegation.save()
        return delegation

    def add_delegation(self, country: str, responses) -> Delegation:
        """
        adds a delegation to the committee
        responses[0], responses[3]: user first name
        responses[1], responses[4]: user last name
        responses[2], responses[5]: user email
        responses[-1]: committee acronym
        """
        delegation = Delegation(country=country)
        delegation.save()
        self.add_delegate(responses[-1], delegation, responses[0], responses[1], responses[2])
        if len(responses) > 3:
            self.add_delegate(responses[-1], delegation, responses[3], responses[4], responses[5], 2)
        self.delegations.add(delegation)
        self.save()
        return delegation

    def __str__(self):
        if self.number_present:
            return f"Simple: {self.simple_majority}, 2/3: {self.super_majority}, Present: {self.number_present}"
        return f"People Manager"
