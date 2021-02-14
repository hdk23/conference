from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    context={}
    return render(request, 'dartmun/index.html', context)


def my_committee(request):
    context = {}
    return render(request, 'dartmun/mycommittee.html', context)
