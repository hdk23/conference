from django.shortcuts import render
from .functions_create_objects import create_committee, reset_committee
from .models import *

# Create your views here.
def index(request):
    """loads the index page"""
    reset_committee()
    create_committee()
    context = {}
    return render(request, 'dartmun/index.html', context)


def my_committee(request):
    """loads the my committee page"""
    committee = Committee.objects.first()
    delegations = committee.delegations.order_by('country')
    context = {"committee": committee, "delegations":delegations}
    return render(request, 'dartmun/mycommittee.html', context)
