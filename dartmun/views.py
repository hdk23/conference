from django.shortcuts import render
from .functions_create_objects import create_committee, reset_committee

# Create your views here.
def index(request):
    """loads the index page"""
    reset_committee()
    create_committee()
    context = {}
    return render(request, 'dartmun/index.html', context)


def my_committee(request):
    """loads the my committee page"""
    context = {}
    return render(request, 'dartmun/mycommittee.html', context)