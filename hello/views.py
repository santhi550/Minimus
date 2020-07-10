from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from push_notifications.models import WebPushDevice 
from .models import Greeting,Items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,auth
from django.contrib import messages
import json

# Create your views here.
def index(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user_id=(User.objects.get(username=username)).id
        items_list=[]
        if WebPushDevice.objects.filter(user_id=user_id):
            items_list=Items.objects.filter(user_id=user_id)
        return render(request, 'index.html', {"username" : username,'items':items_list})
    else:
        return render(request, 'login.html')

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})

@csrf_exempt
def save_push(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user_id=(User.objects.get(username=username)).id
        post_data=json.loads(request.body.decode('utf-8'))
        if WebPushDevice.objects.filter(user_id=user_id):
            WebPushDevice.objects.filter(user_id=user_id).update(user_id=user_id,name=post_data.get('name'),registration_id=post_data.get('registration_id'),p256dh=post_data.get('p256dh'),active=True,auth=post_data.get('auth'),browser='CHROME')
        else:
            WebPushDevice.objects.create(user_id=user_id,name=post_data.get('name'),registration_id=post_data.get('registration_id'),p256dh=post_data.get('p256dh'),active=True,auth=post_data.get('auth'),browser='CHROME')
        
        return HttpResponse("Successfully Subscribed")
    else:
        return HttpResponse("<a href='/login'>Login Again</a>")
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
        if user :
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
def add_item(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user_id=(User.objects.get(username=username)).id
        url=request.POST["url"]
        amount=request.POST["amount"]
        Items.objects.create(url=url,amount=amount,user_id=user_id)
    return  HttpResponseRedirect('/')
def update_item(request):
    if request.session.has_key('user'):
        username = request.session['user']
        user_id=(User.objects.get(username=username)).id
        url=request.POST["url"]
        amount=request.POST["amount"]
        Items.objects.filter(user_id=user_id).update(url=url,amount=amount,user_id=user_id)
    return  HttpResponseRedirect('/')