from django.shortcuts import render


# Create your views here.
def index(request):
    """loads the index page"""
    context={}
    return render(request, 'dartmun/index.html', context)


def my_committee(request):
    """loads the my committee page"""
    context = {}
    return render(request, 'dartmun/mycommittee.html', context)