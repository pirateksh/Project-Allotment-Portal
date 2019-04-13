from django.shortcuts import render
from prof_add.models import *
from lead_allot.models import *
from administrator.models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
# Create your views here.


def returned(request, username):
    choice = request.POST['return']
    admin = Administrator.objects.get(username=username)
    if choice == 'return':
        return render(request, 'administrator/admin_home.html', {'admin': admin})


def home(request):
    if request.method == "POST":
        username = request.POST['username']
        i_am = request.POST['choice']
        # Administrator login
        if i_am == 'admin':
            admins = Administrator.objects.filter(username=username)
            if admins:
                admin = Administrator.objects.get(username=username)
                return render(request, 'administrator/admin_login.html', {'admin': admin})
            else:
                messages.info(request, f"User not found")
                return render(request, 'administrator/home.html', {})
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
                    return render(request, 'administrator/home.html', {})
            else:  # Leaders not yet allotted.
                messages.info(request, f"Group leader login not authorised yet!")
                return render(request, 'administrator/home.html', {})
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
                    return render(request, 'administrator/home.html', {})
            else:  # Student password not yet set.
                messages.info(request, f"Student login not authorised yet!")
                return render(request, 'administrator/home.html', {})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def admin_home(request, username):
    if request.method == 'POST':
        password = request.POST['admin_pass']
        admin = Administrator.objects.get(username=username)
        if check_password(password, admin.password):
            return render(request, 'administrator/admin_home.html', {'admin': admin})
        else:
            messages.info(request, f"Wrong password")
            message = "wrong Password"
            return render(request, 'administrator/admin_login.html', {'admin': admin, 'message': message})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def register_gate(request):
    admin = Administrator.objects.all()
    if admin.count() == 0:
        return render(request, 'administrator/admin_register.html', {})
    else:
        messages.info(request, f"Admin already registered")
        return render(request, 'administrator/home.html', {})


def register_admin(request):
    username = request.POST['admin_user']
    password = request.POST['admin_pass']
    re_password = request.POST['re_admin_pass']
    if password == re_password:
        admin = Administrator(username=username, password=make_password(re_password))
        admin.save()
        messages.success(request, f"Admin registered successfully")
        return render(request, 'administrator/home.html', {})
    else:
        messages.info(request, f"Passwords did not match")
        return render(request, 'administrator/admin_register.html', {})


def stu_pass_set(request, username):
    if request.method == 'POST':
        choice = request.POST['set']
        if choice == 'yes':
            admin = Administrator.objects.get(username=username)
            students = Student.objects.all()
            if students:
                for student in students:
                    student.password = make_password(student.reg_no)
                    student.save()
                admin.is_stu_pass_set = True
                admin.save()
                messages.info(request, f"Default student password has been set")
                return render(request, 'administrator/admin_home.html', {'admin': admin})
            else:
                messages.info(request, f"No student in database yet")
                return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def lead_allot(request, username):
    if request.method == 'POST':
        choice = request.POST['allot']
        if choice == 'yes':
            admin = Administrator.objects.get(username=username)
            if not admin.is_lead_allotted:
                # Calculating total number of groups
                total = 0
                professors = Professor.objects.all()
                if professors:
                    for prof in professors:
                        total += prof.nog
                    # Calculated
                    students = Student.objects.all().order_by('-cpi')
                    if students:
                        i = 1
                        for student in students:
                            if i <= total:
                                lead = Leader(name=student.name, reg_no=student.reg_no, email=student.email, rank=i,
                                              password=make_password(student.reg_no))
                                i += 1
                                lead.save()
                                student.is_lead = True
                                student.save()
                                # Email notification
                                subject = 'Selected as Group Leader'
                                message = 'Hi, '+student.name+'! You have been selected as Group Leader. '
                                message += 'Your current password is your Registration Number. '
                                message += "This is a system generated Email. Don't bother replying."
                                to = student.email
                                try:
                                    send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
                                except BadHeaderError:
                                    messages.info(request, f"Invalid Header found")
                                # Notification sent
                            else:
                                break
                        admin.is_lead_allotted = True
                        admin.save()
                        messages.success(request, f"Leaders assigned successfully")
                        return render(request, 'administrator/admin_home.html', {'admin': admin})
                    else:
                        messages.info(request, f"No student in database yet")
                        return render(request, 'administrator/admin_home.html', {'admin': admin})
                else:
                    messages.info(request, f"No professor in database yet")
                    return render(request, 'administrator/admin_home.html', {'admin': admin})
            else:
                messages.info(request, f"Leaders have already been allotted")
                return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def assign_mentor_round_1(request, username):
    if request.method == 'POST':
        choice = request.POST['assign1']
        if choice == 'yes':
            admin = Administrator.objects.get(username=username)
            leaders = Leader.objects.filter(has_filled_pref=True).order_by('rank')
            for leader in leaders:
                # Getting preferences
                preferences = []
                pri = ""
                for ch in leader.pref_1:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break

                pri = ""
                for ch in leader.pref_2:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break

                pri = ""
                for ch in leader.pref_3:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break
                # Got preferences

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

            # Mail notification

            for lead in leaders:
                if lead.pref_allotted != '0':
                    subject = 'Mentor allotted'
                    message = 'Hi, ' + lead.name + '! Mentor has been allotted to you in Round 1 allotment. '
                    message += 'Visit your profile for more details. '
                    message += "This is a system generated Email. Don't bother replying."
                    to = lead.email
                    try:
                        send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
                    except BadHeaderError:
                        messages.info(request, f"Invalid Header found")
            # Notification sent

            admin.round_1 = True
            admin.save()
            messages.success(request, f"Round 1 allotment successful")
            return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def assign_mentor_round_2(request, username):
    if request.method == 'POST':
        choice = request.POST['assign2']
        if choice == 'yes':
            admin = Administrator.objects.get(username=username)
            leaders = Leader.objects.filter(pref_allotted='0', has_filled_pref=True).order_by('rank')
            for leader in leaders:
                # Getting preferences
                preferences = []
                pri = ""
                for ch in leader.pref_1:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break

                pri = ""
                for ch in leader.pref_2:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break

                pri = ""
                for ch in leader.pref_3:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break
                # Got preferences
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

            # Mail notification

            for lead in leaders:
                if lead.pref_allotted != '0':
                    subject = 'Mentor allotted'
                    message = 'Hi, ' + lead.name + '! Mentor has been allotted to you in Round 2 allotment. '
                    message += 'Visit your profile for more details. '
                    message += "This is a system generated Email. Don't bother replying."
                    to = lead.email
                    try:
                        send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
                    except BadHeaderError:
                        messages.info(request, f"Invalid Header found")
            # Notification sent

            admin.round_2 = True
            admin.save()
            messages.success(request, f"Round 2 allotment successful")
            return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def assign_mentor_round_3(request, username):
    if request.method == 'POST':
        choice = request.POST['assign3']
        if choice == 'yes':
            admin = Administrator.objects.get(username=username)
            leaders = Leader.objects.filter(pref_allotted='0', has_filled_pref=True).order_by('rank')
            for leader in leaders:
                # Getting preferences
                preferences = []
                pri = ""
                for ch in leader.pref_1:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break

                pri = ""
                for ch in leader.pref_2:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break

                pri = ""
                for ch in leader.pref_3:
                    if ch != ',':
                        pri += ch
                    else:
                        preferences += [int(pri)]
                        break
                # Got preferences
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

            # Mail notification

            for lead in leaders:
                if lead.pref_allotted != '0':
                    subject = 'Mentor allotted'
                    message = 'Hi, ' + lead.name + '! Mentor has been allotted to you in Round 3 allotment. '
                    message += 'Visit your profile for more details. '
                    message += "This is a system generated Email. Don't bother replying."
                    to = lead.email
                    try:
                        send_mail(subject, message, 'ksh1998@gmail.com', [to], fail_silently=False)
                    except BadHeaderError:
                        messages.info(request, f"Invalid Header found")
            # Notification sent
            admin.round_3 = True
            admin.is_mentor_assigned = True
            admin.save()
            messages.success(request, f"Round 3 allotment successful")
            return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def developers(request):
    return render(request, 'developers.html', {})


def add_stu_yes_or_no(request):
    if request.method == 'POST':
        admins = Administrator.objects.all()
        admin = admins[0]
        choice = request.POST['choice_stu']
        if choice == 'yes':
            return render(request, 'administrator/add_student.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})


def add_student(request, username):
    if request.method == 'POST':
        admin = Administrator.objects.get(username=username)
        name = request.POST['name']
        reg_no = request.POST['reg_no']
        branch = request.POST['branch']
        cpi = request.POST['cpi']
        email = request.POST['email']
        student = Student(name=name, reg_no=reg_no, branch=branch, cpi=cpi, email=email)
        student.save()
        messages.success(request, f"Student added successfully")
        return render(request, 'administrator/admin_home.html', {'admin': admin})
    else:
        messages.info(request, f"You are not logged in")
        return render(request, 'administrator/home.html', {})
