from django.template import loader, RequestContext
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from datetime import timedelta

from chorizo.models import ChoreType, Chore, ChoreLog
from chorizo.forms import NewUserForm, NewChoreForm

# Create your views here.

def index(request):
    """ index page with handy chore list """
    template = loader.get_template("chorizo/index.html")
    chores = None

    try:
        if request.user.is_authenticated():
            chores = Chore.objects.filter(assignee = request.user).order_by("-due_date")
    except Chore.DoesNotExist:
        pass

    context = RequestContext(request, {
        "chores": chores
    })

    return HttpResponse(template.render(context))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
        else:
            messages.add_message(request, messages.ERROR, "That login and password combination isn't valid")

        return redirect("index")

    if request.method == "GET":
        messages.add_message(request, messages.ERROR, "You must be logged in to do that")
        return redirect("index")

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = request.POST["username"], password = request.POST["password"])
            user.save()
            messages.add_message(request, messages.INFO, "Your account has been set up. Log in now!")
        else:
            messages.add_message(request, messages.ERROR, "We couldn't create that user")
            

    return redirect("index")

@login_required(login_url="/chorizo/login")
def give_chore(request):
    if request.method == "POST":
        form = NewChoreForm(request.POST)
        if form.is_valid():
            chore_description = request.POST.get("chore_description", "some random job")

            c = Chore(description = chore_description, \
              assignee = request.user, \
              assigner = request.user, \
              due_date = timezone.now() + timedelta(3, 0, 0), \
              chore_type = ChoreType.objects.get(id = 1) \
             )
            c.save()
        else:
            messages.add_message(request, messages.ERROR, "I couldn't add that chore to your list")

        return redirect("index")

    if request.method == "GET":
        template = loader.get_template("chorizo/login.html")
        context = RequestContext(request, {
            "next": request.GET["next"]
        })

@login_required(login_url="/chorizo/login")
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "You have been logged out")
    return redirect("index")

@login_required(login_url="chorizo/login")
def complete(request, chore_id):
    try:
        chore = Chore.objects.get(assignee = request.user, id = chore_id)
    except Chore.DoesNotExist:
        raise Http404

    chore.finish()
    return redirect("index")

@login_required(login_url="/chorizo/login")
def details(request, chore_id):
    try:
        chore = Chore.objects.get(id = chore_id, assignee = request.user)
    except Chore.DoesNotExist:
        raise Http404

    template = loader.get_template("chorizo/details.html")
    context = RequestContext(request, {
        "chore": chore
    })
    
    return HttpResponse(template.render(context))
    

