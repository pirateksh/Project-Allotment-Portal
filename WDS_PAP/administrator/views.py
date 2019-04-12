from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from prof_add.models import *
from lead_allot.models import *
from administrator.models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
# Create your views here.


def admin_login_error(request, username):
    admin = Administrator.objects.get(username=username)
    return render(request, 'administrator/admin_login.html', {'admin': admin})


def dummy_admin_home(request, username):
    admin = Administrator.objects.get(username=username)
    return render(request, 'administrator/admin_home.html', {'admin': admin})


def home(request):
    username = request.POST['username']
    i_am = request.POST['choice']
    # Administrator login
    if i_am == 'admin':
        admins = Administrator.objects.filter(username=username)
        if admins:
            admin = admins.get(username=username)
            return render(request, 'administrator/admin_login.html', {'admin': admin})
        else:
            messages.info(request, f"User not found")
            return redirect('home')
    # Group leader login
    elif i_am == 'lead':
        leaders = Leader.objects.filter(reg_no=username)
        admins = Administrator.objects.all()
        admin = admins[0]
        if admin.is_lead_allotted:
            if leaders:
                leader = leaders.get(reg_no=username)
                return render(request, 'lead_allot/leader_login.html', {'leader': leader})
            else:
                messages.info(request, f"User not found")
                return redirect('home')
        else:  # Leaders not yet allotted.
            messages.info(request, f"Group leader login not authorised yet!")
            return redirect('home')
    # Student login
    else:
        students = Student.objects.filter(reg_no=username)
        admins = Administrator.objects.all()
        admin = admins[0]
        if admin.is_stu_pass_set:
            if students:
                student = students.get(reg_no=username)
                return render(request, 'lead_allot/student_login.html', {'student': student})
            else:
                messages.info(request, f"User not found")
                return redirect('home')
        else:  # Student password not yet set.
            messages.info(request, f"Student login not authorised yet!")
            return redirect('home')


def admin_home(request, username):
    password = request.POST['admin_pass']
    admin = Administrator.objects.get(username=username)
    if check_password(password, admin.password):
        return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"Wrong password")
        return HttpResponseRedirect(reverse('Admin Login Error',kwargs={'username': username}))


def register_gate(request):
    admin = Administrator.objects.all()
    if admin.count() == 0:
        return render(request, 'administrator/admin_register.html', {})
    else:
        messages.info(request, f"Admin already registered")
        return HttpResponseRedirect(reverse('home'))


def register_admin(request):
    username = request.POST['admin_user']
    password = request.POST['admin_pass']
    re_password = request.POST['re_admin_pass']
    if password == re_password:
        admin = Administrator(username=username, password=make_password(re_password))
        admin.save()
        return HttpResponseRedirect(reverse('home'))
    else:
        messages.info(request, f"Passwords did not match")
        return HttpResponseRedirect(reverse('Dummy Admin Home', kwargs={'username': username}))


def stu_pass_set(request, username):
    admin = Administrator.objects.get(username=username)
    students = Student.objects.all()
    for student in students:
        student.password = make_password(student.reg_no)
        student.save()
    admin.is_stu_pass_set = True
    admin.save()
    messages.info(request, f"Default password has been set")
    return HttpResponseRedirect(reverse('Dummy Admin Home', kwargs={'username': username}))


def lead_allot(request, username):
    admin = Administrator.objects.get(username=username)
    # Calculating total number of groups
    total = 0
    professors = Professor.objects.all()
    for prof in professors:
        total += prof.nog
    # Calculated
    students = Student.objects.all().order_by('-cpi')
    i = 1
    for student in students:
        if i <= total:
            lead = Leader(name=student.name, reg_no=student.reg_no, email=student.email, rank=i,
                          password=make_password(student.reg_no))
            i += 1
            lead.save()
            student.is_lead = True
            student.save()
            """
            subject = 'Selected as Group Leader'
            message = 'Hi, '+student.name+'! You have been selected as Group Leader. '
            message += 'Your current password is your Registration Number. '
            message += "This is a system generated Email. Don't bother replying."
            to = student.email
            try:
                send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid Header found")
            """
        else:
            break
    admin.is_lead_allotted = True
    admin.save()
    messages.success(request, f"Leaders assigned successfully")
    return HttpResponseRedirect(reverse('Dummy Admin Home', kwargs={'username': username}))


def assign_mentor_round_1(request, username):
    admin = Administrator.objects.get(username=username)
    leaders = Leader.objects.filter(has_filled_pref=True).order_by('rank')
    for leader in leaders:
        preferences = [leader.pref_1[0], leader.pref_2[0], leader.pref_3[0]]
        for pref in preferences:
            prof = Professor.objects.get(pk=pref)
            if prof.is_free:
                leader.pref_allotted = str(prof.pk) + ',' + prof.name
                prof.nog_assigned += 1
                if prof.nog == prof.nog_assigned:
                    prof.is_free = False
                prof.groups_assigned += str(leader.rank) + ','
                leader.save()
                prof.save()
                break
    # If mentor not allotted then deleting preferences.
    left_leaders = Leader.objects.filter(pref_allotted='0').filter(has_filled_pref=True)
    for left_leader in left_leaders:
        left_leader.has_filled_pref = False
        left_leader.save()
    # Preference deletion done
    """
    # Mail notification
    leaders_mail = leaders - left_leaders
    for lead in leaders_mail:
        subject = 'Mentor allotted'
        message = 'Hi, ' + lead.name + '! Mentor has been allotted to you in Round 1 allotment. '
        message += 'Visit your profile for more details. '
        message += "This is a system generated Email. Don't bother replying."
        to = lead.email
        try:
            send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
        except BadHeaderError:
            return HttpResponse("Invalid Header found")
    # Notification sent
    """
    admin.round_1 = True
    admin.save()
    messages.success(request, f"Round 1 allotment successful")
    return HttpResponseRedirect(reverse('Dummy Admin Home', kwargs={'username': username}))


def assign_mentor_round_2(request, username):
    admin = Administrator.objects.get(username=username)
    leaders = Leader.objects.filter(pref_allotted='0', has_filled_pref=True).order_by('rank')
    for leader in leaders:
        preferences = [leader.pref_1[0], leader.pref_2[0], leader.pref_3[0]]
        for pref in preferences:
            prof = Professor.objects.get(pk=pref)
            if prof.is_free:
                leader.pref_allotted = str(prof.pk) + ',' + prof.name
                leader.save()
                prof.nog_assigned += 1
                if prof.nog == prof.nog_assigned:
                    prof.is_free = False
                prof.groups_assigned += str(leader.rank) + ','
                prof.save()
                break

    # If mentor not allotted then deleting preferences.
    left_leaders = Leader.objects.filter(pref_allotted='0').filter(has_filled_pref=True)
    for left_leader in left_leaders:
        left_leader.has_filled_pref = False
        left_leader.save()
    # Preference deletion done
    """
    # Mail notification
    leaders_mail = leaders - left_leaders
    for lead in leaders_mail:
        subject = 'Mentor allotted'
        message = 'Hi, ' + lead.name + '! Mentor has been allotted to you in Round 2 allotment. '
        message += 'Visit your profile for more details. '
        message += "This is a system generated Email. Don't bother replying."
        to = lead.email
        try:
            send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
        except BadHeaderError:
            return HttpResponse("Invalid Header found")
    # Notification sent
    """
    admin.round_2 = True
    admin.save()
    messages.success(request, f"Round 2 allotment successful")
    return HttpResponseRedirect(reverse('Dummy Admin Home', kwargs={'username': username}))


def assign_mentor_round_3(request, username):
    admin = Administrator.objects.get(username=username)
    leaders = Leader.objects.filter(pref_allotted='0', has_filled_pref=True).order_by('rank')
    for leader in leaders:
        preferences = [leader.pref_1[0], leader.pref_2[0], leader.pref_3[0]]
        for pref in preferences:
            prof = Professor.objects.get(pk=pref)
            if prof.is_free:
                leader.pref_allotted = str(prof.pk) + ',' + prof.name
                leader.save()
                prof.nog_assigned += 1
                if prof.nog == prof.nog_assigned:
                    prof.is_free = False
                prof.groups_assigned += str(leader.rank) + ','
                prof.save()
                break

    left_leaders = Leader.objects.filter(pref_allotted='0')
    """
    # Assignment after round 3
    mentors = Professor.objects.filter(is_free=True)
    k = 0
    for mentor in mentors:
        while mentor.is_free:
            left_leader = left_leaders[k]
            left_leader.pref_allotted = str(mentor.pk) + ',' + mentor.name
            left_leader.save()
            mentor.nog_assigned += 1
            if mentor.nog == mentor.nog_assigned:
                mentor.is_free = False
            mentor.groups_assigned += str(left_leader.rank) + ','
            mentor.save()
        k += 1
    # Assignment completed
    """
    """
    # Mail notification
    leaders_mail = leaders - left_leaders
    for lead in leaders_mail:
        subject = 'Mentor allotted'
        message = 'Hi, ' + lead.name + '! Mentor has been allotted to you in Round 3 allotment. '
        message += 'Visit your profile for more details. '
        message += "This is a system generated Email. Don't bother replying."
        to = lead.email
        try:
            send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
        except BadHeaderError:
            return HttpResponse("Invalid Header found")
    # Notification sent
    """
    admin.round_3 = True
    admin.is_mentor_assigned = True
    admin.save()
    messages.success(request, f"Round 3 allotment successful")
    return HttpResponseRedirect(reverse('Dummy Admin Home', kwargs={'username': username}))
