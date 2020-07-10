from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from push_notifications.models import WebPushDevice 
from .models import Greeting
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.contrib import messages
import json

# Create your views here.
def index(request):
    if request.session.has_key('user'):
        username = request.session['user']
        return render(request, 'index.html', {"username" : username})
    else:
        return render(request, 'login.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

@csrf_exempt
def save_push(request):
    post_data=json.loads(request.body.decode('utf-8'))
    WebPushDevice.objects.create(name=post_data.get('name'),registration_id=post_data.get('registration_id'),p256dh=post_data.get('p256dh'),active=True,auth=post_data.get('auth'),browser='CHROME')
    return HttpResponse("done")
def login(request):
    if request.method =='GET':
        return render(request,'login.html')
    if request.method == 'POST':
        username=request.POST["username"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=username,password=pwd)
        if user is not None:
            request.session['user'] = username
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return  HttpResponseRedirect('/login')
def signup(request):
    if request.method =='GET':
        return render(request,"signup.html")
    if request.method=='POST':
        username=request.POST["email"]
        psw=request.POST["psw"]
        user=User.objects.filter(username=username)
        if user is not None:
            messages.info(request,'User Already Exisits')
            return HttpResponseRedirect('/signup')
        else:
            user=User.objects.create_user(username=username,password=psw,email=username)
            user.save()
            return  HttpResponseRedirect('/login')
def logout(request):
    try:
        del request.session['user']
    except:
        pass
    auth.logout(request)
    return  HttpResponseRedirect('/')