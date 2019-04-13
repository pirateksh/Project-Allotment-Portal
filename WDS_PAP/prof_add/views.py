from django.shortcuts import render
from prof_add.models import *
from administrator.models import *
from django.contrib import messages
# Create your views here.


def prof_add_or_not(request):
    if request.method == 'POST':
        choice = request.POST['choice']
        if choice == 'yes':
            admins = Administrator.objects.all()
            admin = admins[0]
            return render(request, "prof_add/prof_entry.html", {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def professor(request, username):
    admin = Administrator.objects.get(username=username)
    professors = Professor.objects.all()
    name = request.POST['name']
    dept = request.POST['dept']
    email = request.POST['email']
    group = request.POST['group']
    aoi = request.POST['aoi']
    for sir in professors:
        if email == sir.email:
            messages.error(request, f"Professor already added")
            return render(request, "prof_add/prof_entry.html", {'admin': admin})
    prof = Professor(name=name, dept=dept, aoi=aoi, email=email, nog=group)
    prof.save()
    messages.success(request, f"Professor Added successfully!")
    return render(request, 'administrator/admin_home.html', {'admin': admin})

