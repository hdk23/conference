from .models_people import *
from django.db import models
from django_countries import countries
import pycountry


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
    def add_user(first: str, last: str, email: str, username: str, staff=False, superuser=False) -> User:
        """adds a user to the database"""
        user = User.objects.create_user(username, email, 'dartmun2021')
        user.first_name = first
        user.last_name = last
        user.is_staff = staff
        user.is_superuser = superuser
        user.save()
        return user

    def add_chair(self, user: User, chair_type: str, year: int):
        """adds a chair to the people manager"""
        chair = Chair(user=user, year=year)
        chair.save()
        if chair_type == "CD":
            cd = CommitteeDirector(chair=chair)
            cd.save()
            self.directors.add(cd)
            self.save()
        else:
            cm = CommitteeManager(chair=chair)
            cm.save()
            self.managers.add(cm)
            self.save()


    def add_delegate(self, user, country_string, school=None, number=1) -> Delegate:
        """adds a delegate to a delegation"""
        delegate = Delegate(user=user, number=number)
        delegate.save()
        try:
            country = pycountry.countries.get(name=country_string).alpha_2
        except:
            country = pycountry.countries.get(common_name=country_string).alpha_2
        try:
            delegation = self.delegations.get(country=country)
        except:
            school = School.objects.get(name=school)
            delegation = Delegation(country=country, school=school)
            delegation.save()
            self.delegations.add(delegation)
            self.save()
            school.delegations.add(delegation)
            school.save()
        delegation.delegates.add(delegate)
        delegation.save()
        return delegate

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
        username = f"{responses[-1]}{country}".replace(" ", "").lower()
        user = self.add_user(responses[0], responses[1], username, responses[2])
        self.add_delegate(user, country)
        if len(responses) > 4:
            username2 = f"{responses[-1]}{country}2".replace(" ", "").lower()
            user2 = self.add_user(responses[3], responses[4], username2, responses[5])
            self.add_delegate(user2, country, number=2)
        self.delegations.add(delegation)
        self.save()
        return delegation

    def reset(self):
        self.quorum = None
        self.simple_majority = None
        self.super_majority = None
        self.min_signatory = None
        self.number_present = 0
        self.save()

    def __str__(self):
        if self.number_present:
            return f"Simple: {self.simple_majority}, 2/3: {self.super_majority}, Present: {self.number_present}"
        return f"People Manager"
