from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from bulletin.forms import *
from bulletin.models import *
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,logout
from django.contrib import auth

# Create your views here.

class ExampleView(View):
    def get(self, request):
        return render(request, 'base.html')

class BulletsView(ListView):
    model = Bullet
    context_object_name = 'bullets'
    template_name = 'bullets.html'
    
    def get_queryset(self):
        qs = Bullet.objects.all().order_by('-datetime')#.values()
        return qs

class BulletView(View):
    def get(self, request, id):
        data = Bullet.objects.get(id__exact=id)
        return render(request, 'bullet.html', {'bullet':data})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #return redirect(reverse('bullets'))
            return authorization(request)
        return render(request, 'signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

def authorization(request):
    redirect_url = reverse('bullets')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['login'],
                                     password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, 'Wrong login or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form, 'continue': redirect_url})

@login_required
def exit(request):
    logout(request)
    return render(request, 'logout.html')
