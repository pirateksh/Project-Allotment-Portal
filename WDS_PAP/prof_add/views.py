from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from prof_add.models import *
from lead_allot.models import *
from administrator.models import *
# Create your views here.


def prof_add_or_not(request):
    admins = Administrator.objects.all()
    admin = admins[0]
    return render(request, "prof_add/prof_entry.html", {'admin': admin})


def professor(request):
    name = request.POST['name']
    dept = request.POST['dept']
    email = request.POST['email']
    group = request.POST['group']
    aoi = request.POST['aoi']
    prof = Professor(name=name, dept=dept, aoi=aoi, email=email, nog=group)
    prof.save()
    return HttpResponse("Professor Added successfully!")
