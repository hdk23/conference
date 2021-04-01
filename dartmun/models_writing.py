from django.db import models
from .models_people import Delegation


class SponSig(models.Model):
    """model with methods related to sponsors and signatories that overlap between WPs and resos"""
    sponsors = models.ManyToManyField(Delegation, related_name="sponsors")
    signatories = models.ManyToManyField(Delegation, related_name="signatories")

    def add_sponsors(self, sponsor_ids):
        """receives a list of delegation ids and adds the corresponding delegates as sponsors"""
        for sponsor in sponsor_ids:
            delegation = Delegation.objects.get(pk=int(sponsor))
            self.sponsors.add(delegation)
        self.save()

    def add_signatories(self, signatory_ids):
        """receives a list of delegation ids and adds the corresponding delegates as signatories"""
        for signatory in signatory_ids:
            delegation = Delegation.objects.get(pk=int(signatory))
            self.signatories.add(delegation)
        self.save()

    def get_sponsors(self):
        """returns the list of sponsors in a readable list"""
        string = ""
        for sponsor in self.sponsors.order_by('country'):
            string = f"{string} {sponsor.country.name},"
        return string[:-1]

    def get_signatories(self):
        """returns the list of signatories in a readable list"""
        string = ""
        for signatory in self.signatories.order_by('country'):
            string = f"{string} {signatory.country.name},"
        return string[:-1]

    def __str__(self):
        return f"Sponsors: {self.get_sponsors()}"


class WorkingPaper(models.Model):
    """Working Paper model to represent a working paper"""
    sponsig = models.OneToOneField(SponSig, null=True, blank=True, on_delete=models.CASCADE)
    introduced = models.BooleanField(default=False)

    def __str__(self):
        return f"Working Paper by {self.sponsig.get_sponsors()}"


class Amendment(models.Model):
    """Amendment model to represent an amendment"""
    TYPE_CHOICES = [('A', 'Add'), ('M', 'Modify'), ('S', 'Strike')]
    amendment_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    clause = models.CharField(max_length=16)
    friendly = models.BooleanField(default=False)
    score = models.PositiveSmallIntegerField()
    old = models.TextField(null=True, blank=True)
    new = models.TextField(null=True, blank=True)
    sponsig = models.OneToOneField(SponSig, null=True, blank=True, on_delete=models.CASCADE)
    introduced = models.BooleanField(default=False)
    votes_for = models.PositiveSmallIntegerField(null=True)
    votes_against = models.PositiveSmallIntegerField(null=True)
    votes_abstain = models.PositiveSmallIntegerField(null=True)
    passed = models.BooleanField(null=True)

    def passes(self, votes_for, votes_against, votes_abstain):
        """calculates whether the motion passes"""
        self.votes_for = votes_for
        self.votes_against = votes_against
        self.votes_abstain = votes_abstain
        self.passed = self.votes_for > self.votes_against
        self.save()

    def __str__(self):
        if self.amendment_type == "A":
            amend_type = "Add"
        elif self.amendment_type == "M":
            amend_type = "Modify"
        else:
            amend_type = "Strike"
        return f"{amend_type} Clause {self.clause} by {self.sponsig.sponsors.first().country.name}"


class Resolution(models.Model):
    """Resolution model to represent a resolution"""
    sponsig = models.OneToOneField(SponSig, null=True, blank=True, on_delete=models.CASCADE)
    introduced = models.BooleanField(default=False)
    votes_for = models.PositiveSmallIntegerField(null=True)
    votes_against = models.PositiveSmallIntegerField(null=True)
    votes_abstain = models.PositiveSmallIntegerField(null=True)
    passed = models.BooleanField(null=True)
    amendments = models.ManyToManyField(Amendment)

    def passes(self, votes_for: int, votes_against: int, votes_abstain=0):
        """calculates whether the motion passes"""
        self.votes_for = votes_for
        self.votes_against = votes_against
        self.votes_abstain = votes_abstain
        self.passed = self.votes_for > self.votes_against
        self.save()

    def add_amend(self, amend_type, clause, friendly, score, sponsor_id, signatory_ids):
        """adds an amendment to a resolution"""
        amendment = Amendment(amendment_type=amend_type, clause=clause, friendly=friendly, score=score)
        if not friendly:
            amendment.score += score
        sponsig = SponSig()
        sponsig.save()
        sponsig.add_sponsors([sponsor_id])
        sponsig.add_signatories(signatory_ids)
        sponsig.save()
        amendment.sponsig = sponsig
        amendment.save()
        self.amendments.add(amendment)
        self.save()

    def unintroduced_amends(self):
        """returns a list of amendments that have not been introduced"""
        amends = []
        for amend in self.amendments.all():
            if not amend.introduced:
                amends.append(amend)
        return amends

    def __str__(self):
        return f"Resolution by {self.sponsig.get_sponsors()}"
