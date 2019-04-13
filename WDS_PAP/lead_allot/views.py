from django.shortcuts import render
from lead_allot.models import Student, Leader
from prof_add.models import Professor
from administrator.models import Administrator
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
# Create your views here.


def getting_invited_students(leader):
    pri = ""
    keys = []
    for ch in leader.invited:
        if ch != ',':
            pri += ch
        else:
            keys += [int(pri)]
            pri = ""
    return Student.objects.filter(pk__in=[key for key in keys])


def getting_accepted_invitee(leader):
    pri = ""
    keys = []
    for ch in leader.accepted_by:
        if ch != ',':
            pri += ch
        else:
            keys += [int(pri)]
            pri = ""
    return Student.objects.filter(pk__in=[key for key in keys])


def getting_invitor_leader(student):
    pri = ""
    keys = []
    for ch in student.invited_by:
        if ch != ',':
            pri += ch
        else:
            keys += [int(pri)]
            pri = ""
    return Leader.objects.filter(rank__in=[key for key in keys])


def returned_lead(request, lead_reg_no):
    choice = request.POST['return_lead']
    if choice == 'return':
        leader = Leader.objects.get(reg_no=lead_reg_no)
        admins = Administrator.objects.all()
        admin = admins[0]
        professors = Professor.objects.all()
        invited_students = getting_invited_students(leader)
        accepted_invitees = getting_accepted_invitee(leader)
        students = Student.objects.filter(is_lead=False)
        if leader.pref_allotted != '0':
            preferences = []
            pri = ""
            for ch in leader.pref_allotted:
                if ch != ',':
                    pri += ch
                else:
                    preferences += [int(pri)]
                    break
            allotted = preferences[0]
            mentor = Professor.objects.get(pk=int(allotted))
        else:
            mentor = 'none'
        context = {
            'leader': leader,
            'professors': professors,
            'invited_students': invited_students,
            'accepted_invitees': accepted_invitees,
            'mentor': mentor,
            'admin': admin,
            'students': students,
        }
        return render(request, 'lead_allot/leader_home.html', context)


def leader_home(request, lead_reg_no):
    if request.method == 'POST':
        password = request.POST['lead_pass']
        leader = Leader.objects.get(reg_no=lead_reg_no)
        admins = Administrator.objects.all()
        admin = admins[0]
        students = Student.objects.filter(is_lead=False)
        if check_password(password, leader.password):
            professors = Professor.objects.all()
            if leader.pref_allotted != '0':
                preferences = []
                pri = ""
                for ch in leader.pref_allotted:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break
                allotted = preferences[0]
                mentor = Professor.objects.get(pk=int(allotted))
            else:
                mentor = 'none'

            # Getting invited students
            invited_students = getting_invited_students(leader)
            # Got invited students
            # Getting accepted invitee
            accepted_invitees = getting_accepted_invitee(leader)
            # Got accepted invitee
            context = {
                'leader': leader,
                'professors': professors,
                'invited_students': invited_students,
                'accepted_invitees': accepted_invitees,
                'mentor': mentor,
                'admin': admin,
                'students': students,
            }
            return render(request, 'lead_allot/leader_home.html', context)
        else:
            messages.info(request, f"Wrong password")
            return render(request, 'lead_allot/leader_login.html', {'leader': leader})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def student_home(request, stu_reg_no):
    if request.method == 'POST':
        password = request.POST['stu_pass']
        student = Student.objects.get(reg_no=stu_reg_no)
        if check_password(password, student.password):
            # Getting invitor leader
            leaders = getting_invitor_leader(student)
            # Got invitor leaders
            context = {
                'leaders': leaders,
                'student': student,
            }
            return render(request, 'lead_allot/student_home.html', context)
        else:
            messages.info(request, f"Wrong password")
            return render(request, 'lead_allot/student_login.html', {'student': student})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def lead_change_password(request, lead_reg_no):
    if request.method == 'POST':
        new_pass = request.POST['new_pass']
        re_pass = request.POST['re_pass']
        leader = Leader.objects.get(reg_no=lead_reg_no)
        if new_pass == re_pass:
            leader.password = make_password(new_pass)
            leader.save()
            messages.success(request, f"Password successfully changed. Login again")
            return render(request, 'lead_allot/leader_login.html', {'leader': leader})
        else:
            admins = Administrator.objects.all()
            admin = admins[0]
            professors = Professor.objects.all()
            invited_students = getting_invited_students(leader)
            accepted_invitees = getting_accepted_invitee(leader)
            students = Student.objects.filter(is_lead=False)
            if leader.pref_allotted != '0':
                preferences = []
                pri = ""
                for ch in leader.pref_allotted:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break
                allotted = preferences[0]
                mentor = Professor.objects.get(pk=int(allotted))
            else:
                mentor = 'none'
            context = {
                'leader': leader,
                'professors': professors,
                'invited_students': invited_students,
                'accepted_invitees': accepted_invitees,
                'mentor': mentor,
                'admin': admin,
                'students': students,
            }
            messages.info(request, f"Passwords did not match. Try Again")
            return render(request, 'lead_allot/leader_home.html', context)
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def stu_change_password(request, stu_reg_no):
    if request.method == 'POST':
        new_pass = request.POST['new_pass']
        re_pass = request.POST['re_pass']
        student = Student.objects.get(reg_no=stu_reg_no)
        if new_pass == re_pass:
            student.password = make_password(new_pass)
            student.save()
            messages.success(request, f"Password successfully changed. Login again")
            return render(request, 'lead_allot/student_login.html', {'student': student})
        else:
            leaders = getting_invitor_leader(student)
            context = {
                'leaders': leaders,
                'student': student,
            }
            messages.info(request, f"Passwords did not match. Try Again")
            return render(request, 'lead_allot/student_home.html', context)
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def invite(request, lead_reg_no, stu_reg_no):
    student = Student.objects.get(reg_no=stu_reg_no)
    leader = Leader.objects.get(reg_no=lead_reg_no)
    admins = Administrator.objects.all()
    admin = admins[0]
    professors = Professor.objects.all()
    invited_students = getting_invited_students(leader)
    accepted_invitees = getting_accepted_invitee(leader)
    students = Student.objects.filter(is_lead=False)
    if leader.pref_allotted != '0':
        preferences = []
        pri = ""
        for ch in leader.pref_allotted:
            if ch != ',':
                pri += ch
            else:
                preferences += [int(pri)]
                break
        allotted = preferences[0]
        mentor = Professor.objects.get(pk=int(allotted))
    else:
        mentor = 'none'
    if student in invited_students:
        context = {
            'leader': leader,
            'professors': professors,
            'invited_students': invited_students,
            'accepted_invitees': accepted_invitees,
            'mentor': mentor,
            'admin': admin,
            'students': students,
        }
        message = student.name + ' has already been invited'
        messages.info(request, message)
        return render(request, 'lead_allot/leader_home.html', context)
    else:
        # Email notification
        subject = 'Invitation'
        message = 'Hi, ' + student.name + '! You are invited to join. '+leader.name+'('+leader.reg_no+")'s group."
        message += ' Accept invite by logging in to your account. First time login password is your registration number'
        message += ". This is a system generated Email. Don't bother replying."
        to = student.email
        try:
            send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
        except BadHeaderError:
            messages.info(request, f"Invalid Header found")
        # Notification sent
        leader.invited += str(student.pk) + ','
        leader.save()
        student.invited_by += str(leader.rank) + ','
        student.save()
        invited_students = getting_invited_students(leader)
        context = {
            'leader': leader,
            'professors': professors,
            'invited_students': invited_students,
            'accepted_invitees': accepted_invitees,
            'mentor': mentor,
            'admin': admin,
            'students': students,
        }
        message = student.name + ' invited successfully'
        messages.success(request, message)
        return render(request, 'lead_allot/leader_home.html', context)


def preference(request, lead_reg_no):
    if request.method == 'POST':
        pref_1 = request.POST['pref_1']
        pref_2 = request.POST['pref_2']
        pref_3 = request.POST['pref_3']
        leader = Leader.objects.get(reg_no=lead_reg_no)
        if not leader.has_filled_pref:
            prof_1 = Professor.objects.get(pk=pref_1)
            prof_2 = Professor.objects.get(pk=pref_2)
            prof_3 = Professor.objects.get(pk=pref_3)
            leader.pref_1 = pref_1 + ',' + prof_1.name
            leader.pref_2 = pref_2 + ',' + prof_2.name
            leader.pref_3 = pref_3 + ',' + prof_3.name
            leader.has_filled_pref = True
            leader.save()
            context = {
                'prof_1': prof_1,
                'prof_2': prof_2,
                'prof_3': prof_3,
                'leader': leader,
            }
            return render(request, 'lead_allot/pref_set.html', context)
        else:
            admins = Administrator.objects.all()
            admin = admins[0]
            professors = Professor.objects.all()
            invited_students = getting_invited_students(leader)
            accepted_invitees = getting_accepted_invitee(leader)
            students = Student.objects.filter(is_lead=False)
            if leader.pref_allotted != '0':
                preferences = []
                pri = ""
                for ch in leader.pref_allotted:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break
                allotted = preferences[0]
                mentor = Professor.objects.get(pk=int(allotted))
            else:
                mentor = 'none'
            context = {
                'leader': leader,
                'professors': professors,
                'invited_students': invited_students,
                'accepted_invitees': accepted_invitees,
                'mentor': mentor,
                'admin': admin,
                'students': students,
            }
            messages.info(request, f"Preferences already filled")
            return render(request, 'lead_allot/leader_home.html', context)
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def accept_invite(request, lead_reg_no, stu_reg_no):
    leader = Leader.objects.get(reg_no=lead_reg_no)
    student = Student.objects.get(reg_no=stu_reg_no)
    leaders = getting_invitor_leader(student)
    context = {
        'leaders': leaders,
        'student': student,
    }
    if student.grp_no == 0:
        leader.accepted_by += str(student.pk) + ','
        student.grp_no = leader.rank
        student.is_avail = False
        leader.save()
        student.save()
        # Email notification
        subject = 'Invitation accepted'
        message = student.name+'('+student.reg_no+') has accepted your invitation.'
        message += "This is a system generated Email. Don't bother replying."
        to = leader.email
        try:
            send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
        except BadHeaderError:
            messages.info(request, f"Invalid Header found")
        # Notification sent
        message = "You are now in "+leader.name+"'s team."
        messages.info(request, message)
        return render(request, 'lead_allot/student_home.html', context)
    else:
        messages.info(request, f"You have already accepted an invitation")
        return render(request, 'lead_allot/student_home.html', context)
