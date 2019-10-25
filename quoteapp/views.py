from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.registervalidator(request.POST)
    print(errors)
    if len(errors) > 0:
       for key, value in errors.items():
           messages.error(request, value)
       return redirect('/')
    passwordFromForm = request.POST['password']
    hashed_password = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
    newuser = User.objects.create(email = request.POST['email'], password = hashed_password.decode())
    print(newuser)
    request.session['loggedinUserID'] = newuser.id
    return redirect('/success')
def home(request):
    loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
    userfavs = loggedinUser.favoritelist
    context = {
        "steak" : Quote.objects.filter(favorite = loggedinUser),
        "pasta" : Quote.objects.exclude(favorite = loggedinUser)
    }
    return render (request, "home.html", context)
def login(request):
    errors = User.objects.loginvalidator(request.POST)
    print(errors)
    if len(errors) > 0:
       for key, value in errors.items():
           messages.error(request, value)
       return redirect('/')
    else:
        loggedinuser = User.objects.filter(email = request.POST['email'])
        loggedinuser = loggedinuser[0]
        request.session['loggedinUserID'] = loggedinuser.id
        return redirect("/success")
def logout(request):
    request.session.clear
    return redirect('/')
def success(request):
    loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
    return render(request, "success.html")
def addquote(request):
    errors = Quote.objects.quotevalidator(request.POST)
    print (errors)
    if len (errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')
    else:
        loggedinuser = User.objects.get(id=request.session['loggedinUserID'])
        Quote.objects.create(quoted = request.POST['quoter'], quotetxt = request.POST['quotetxt'], creator = loggedinuser)
        return redirect('/home')
def addfav(request, id):
    loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
    this_user = loggedinUser
    this_quote = Quote.objects.get(id=id)
    this_user.favoritelist.add(this_quote)
    return redirect('/home')
def deletefav(request, id):
    loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
    this_user = loggedinUser
    this_quote = Quote.objects.get(id=id)
    this_user.favoritelist.remove(this_quote)
    return redirect('/home')
def openeditquote(request, id):
    loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
    return render(request, "quoteedit.html")
def editquote(request, id, method="POST"):
    thisq = Quote.objects.get(id=id)
    context2 = {
        "thisquote" : thisq 
    }
    
    quote_to_update = Quote.objects.get(id=id)
    
    quote_to_update.quoted = request.POST['newqd']
    quote_to_update.quotetxt = request.POST['newq']
    quote_to_update.save()

    return redirect('/home', context2)
def viewquote(request, id):
    loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
    
    thisq = Quote.objects.get(id=id)
    context2 = {
        "thisquote" : thisq 
    }

    return render(request, 'viewquote.html', context2)