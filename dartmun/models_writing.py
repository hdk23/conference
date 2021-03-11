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
    TYPE_CHOICES = [('A', 'Add'), ('M', 'Modify'), ('S', 'Strike')]
    amendment_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    clause = models.PositiveSmallIntegerField()
    subclause = models.CharField(max_length=2)  # number
    subsubclause = models.CharField(max_length=5)  # letter
    friendly = models.BooleanField(default=False)  # roman numeral
    score = models.PositiveSmallIntegerField()
    old = models.TextField(null=True, blank=True)
    new = models.TextField(null=True, blank=True)
    sponsor = models.ForeignKey(Delegation, on_delete=models.CASCADE, related_name="amend_sponsor")
    signatories = models.ManyToManyField(Delegation, related_name="amend_signatories")
    passed = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.amendment_type} Clause {self.clause}.{self.subclause}.{self.subsubclause} by {self.sponsor.country.name}"


class Resolution(models.Model):
    """Resolution model to represent a resolution"""
    sponsig = models.OneToOneField(SponSig, null=True, blank=True, on_delete=models.CASCADE)
    introduced = models.BooleanField(default=False)
    votes_for = models.PositiveSmallIntegerField(null=True)
    votes_against = models.PositiveSmallIntegerField(null=True)
    votes_abstain = models.PositiveSmallIntegerField(null=True)
    passed = models.BooleanField(null=True)
    amendments = models.ManyToManyField(Amendment)

    def passes(self):
        """calculates whether the motion passes"""
        self.passed = self.votes_for > self.votes_against
        self.save()

    def __str__(self):
        return f"Resolution by {self.sponsig.get_sponsors()}"


class WritingManager(models.Model):
    """Writing Manager class to handle working papers and resolutions"""
    current_wp = models.ForeignKey(WorkingPaper, on_delete=models.CASCADE, null=True, blank=True, related_name="current_wp")
    current_reso = models.ForeignKey(Resolution, on_delete=models.CASCADE, null=True, blank=True, related_name="current_reso")
    current_amend = models.ForeignKey(Amendment, on_delete=models.CASCADE, null=True, blank=True, related_name="current_amend")

    def __str__(self):
        if self.current_wp:
            return f"Current WP: {self.current_wp}"
        elif self.current_reso:
            return f"Current Reso: {self.current_reso}"
        elif self.current_amend:
            return f"Current Amend:{self.current_amend}"
        else:
            return f"Writing Manager"