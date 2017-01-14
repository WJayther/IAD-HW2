from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from bulletin.forms import RegistrationForm, BulletForm, LoginForm
from bulletin.models import MyUser, Bullet
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout
from django.contrib import auth

# Create your views here.


class ExampleView(View):
    def get(self, request):
        return render(request, 'base.html')


class BulletsView(ListView):
    model = Bullet
    context_object_name = 'bullets'
    template_name = 'bullets.html'
    paginate_by = 5

    def get_queryset(self):
        qs = Bullet.objects.all().order_by('-datetime')
        return qs


class BulletView(View):
    def get(self, request, id):
        data = Bullet.objects.get(id__exact=id)
        return render(request, 'bullet.html', {'bullet': data})


class UsersView(ListView):
    context_object_name = 'users'
    template_name = 'users.html'

    def get_queryset(self):
        qs = auth.get_user_model().objects.all().order_by('-date_joined')
        return qs


class UserView(View):
    def get(self, request, id):
        data = auth.get_user_model().objects.get(id__exact=id)
        bullets = list(data.bullets.all())
        for followed in data.follows.all():
            for bullet in followed.bullets.all():
                bullets.append(bullet)
        return render(
           request,
           'user.html',
           {
              'selected_user': data,
              'wall_bullets': sorted(
                 bullets,
                 key=lambda b: b.datetime,
                 reverse=True
              )
           }
        )


@login_required
def user_follows(request, id, fid):
    if id == fid:
        return HttpResponse('Нельзя подписаться на самого себя и баловаться с адресной строкой')
    fer_user = MyUser.objects.filter(id__exact=id)[0]
    fed_user = MyUser.objects.filter(id__exact=fid)[0]
    if fed_user in fer_user.follows.all():
        return HttpResponse('Вы уже подписаны на него')
    fer_user.follows.add(fed_user)
    return HttpResponse('Вы успешно подписались на {}'.format(
       fed_user.get_username()
    ))


@login_required
def user_unfollows(request, id, fid):
    if id == fid:
        return HttpResponse(
           'Нельзя отписаться от самого себя и баловаться с адресной строкой'
        )
    fer_user = MyUser.objects.filter(id__exact=id)[0]
    fed_user = MyUser.objects.filter(id__exact=fid)[0]
    if fed_user in fer_user.follows.all():
        fer_user.follows.remove(fed_user)
        return HttpResponse('Вы отписались от {}'.format(
           fed_user.get_username()
        ))
    return HttpResponse('Вы не были подписаны на {}'.format(
       fed_user.get_username()
    ))


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return authorization(request)
        return render(request, 'signup.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def post_bullet(request):
    instance = Bullet(user_posted=request.user)
    if request.method == 'POST':
        form = BulletForm(request.POST)
        if form.is_valid():
            bullet = form.save(commit=False)
            bullet.user_posted = request.user
            print(bullet.user_posted.id)
            bullet.save()
            return redirect(reverse('bullets'))
        return render(request, 'post_bullet.html', {'form': form})
    else:
        form = BulletForm()
    return render(request, 'post_bullet.html', {'form': form})


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
    return render(
       request,
       'login.html',
       {'form': form, 'continue': redirect_url}
    )


@login_required
def exit(request):
    logout(request)
    return render(request, 'logout.html')
