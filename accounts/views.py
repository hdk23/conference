from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('my_committee'))
    else:
        context = {}
        context['message'] = "Invalid credentials. Please try again."
        return render(request, 'registration/login.html', context)


@login_required
def password_change_done(request):
    return HttpResponseRedirect(reverse('settings'))


@login_required(login_url='/admin/login/')
def settings(request):
    return render(request, 'registration/settings.html')


@login_required(login_url='/admin/login/')
def update_info(request):
    first = request.POST.get("first")
    last = request.POST.get("last")
    email = request.POST.get("email")
    user = User.objects.get(username=request.user.username)
    user.first_name = first
    user.last_name = last
    user.email = email
    user.save()
    return HttpResponseRedirect(reverse('settings'))