from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,logout
from django.contrib import auth

# Create your views here.

class ExampleView(View):
    def get(self, request):
        return render(request, 'base.html')
