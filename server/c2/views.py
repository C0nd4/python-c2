from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *

def clientTest(request):
    return HttpResponse(request.META['REMOTE_ADDR'])

def commands(request, uuid):
    return HttpResponse(request.META['REMOTE_ADDR'] + ": " + uuid)
