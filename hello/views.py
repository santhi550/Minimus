from django.shortcuts import render
from django.http import HttpResponse
from push_notifications.models import WebPushDevice 
from .models import Greeting
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

@csrf_exempt
def save_push(request):
    post_data=json.loads(request.body.decode('utf-8'))
    WebPushDevice.objects.create(name=post_data.get('name'),registration_id=post_data.get('registration_id'),p256dh=post_data.get('p256dh'),active=True,auth=post_data.get('auth'),browser='Chrome')
    return HttpResponse("done")