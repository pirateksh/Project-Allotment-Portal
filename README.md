# Project Allotment Portal

## Project Description
Automating the process of mentor assignment and groups formation during the project allotment.

## Salient Features
* Administrator registration / login.
* Group Leader / Student Login.
* Admin can add professors and students.
* Admin can trigger Group Leader Selection (Group Leaders will be selected based on CPI).
* Admin can trigger Mentor Allotment Process (Mentor will be alloted based on specified Algorithm).
* Group Leaders can fill preferance for mentors.
* Group Leaders can invite students to join their group.
* Students can accept Invitation to join group.
* Mentor Allotment in 3 Rounds according to Algorithm (preference given to Group Leaders with higher CPI).
* E-mail sent when mentor is alloted, invitation is received / accepted.
* Chat Room Feature.

## Screenshots of Website

* Home Page
![Image of Homepage](https://drive.google.com/uc?export=view&id=1UMyBBABnnXFTSuMWQVD-v85IlknSh6xH)

* Admin Registration
![Image of Admin Registration](https://drive.google.com/uc?export=view&id=1M9Qc_i5ZzYwLUYnAtHnFR-pOll7l3Ew9)

* Admin Account
![Image of Admin Account](https://drive.google.com/uc?export=view&id=1UXq7-YeCZ4IagKmJeXhZiv5MycgG068r)

* Add professors
![Image of Add professors](https://drive.google.com/uc?export=view&id=1AORyOqX5jlOfhD3i7TRgAGqSGXNcvTPm)

* Add students
![Image of Add students](https://drive.google.com/uc?export=view&id=1ifVgzJ9wj3FGr7rb4g6FoAr_Cv6u_kpv)

* Leader Account
![Image of Leader Account](https://drive.google.com/uc?export=view&id=1ho8NA6G7w1yZCYFQ3qaQXI-rVp6oAbxm)

* Page after filling of Mentor Preferance by Leader for Round 1 Allotment
![Image of Page after filling of Mentor Preferance by Leader for Round 1 Allotment](https://drive.google.com/uc?export=view&id=1iQpQtv_54OMHlSH7S0sA414HXz_Kt2RI)

* Available students to invite (By Group Leader)
![Image of Available students to invite](https://drive.google.com/uc?export=view&id=1TamyIqwimnVal-khS0K1axMV-r2xj1BK)

* After Inviting Student
![Image of After Inviting Student](https://drive.google.com/uc?export=view&id=12WCN6qhV5bhy49N4qDWjysshK-UvbEWA)

* Student Account
![Image of Student Account](https://drive.google.com/uc?export=view&id=1D2lBpkeO35rmuU3FjniUQ8pePjs1MHfE)

* Student Account after accepting invitation for joining group.
![Image of Student Account after accepting invitation for joining group.](https://drive.google.com/uc?export=view&id=1vfMh8Fd6hfc909QwL6bpCsdsUGlMChkJ)

* Entering Chat Room
![Image of Entering Chat Room](https://drive.google.com/uc?export=view&id=1XhHPrZo1iTx8cAd_Rwg38tjO5yyOFxWK)

* Chat Room
![Image of Chat Room](https://drive.google.com/uc?export=view&id=1VCK-gOGp6K78RCBXxBGk05aoVR_ODJa4)

* Selected as Group Leader Email
![Image of Selected as Group Leader Email](https://drive.google.com/uc?export=view&id=112dbzHAtZw-RgXLv6woy672jiMVHrJWh)

* Mentor Allotment Email
![Image of Mentor Allotment Email](https://drive.google.com/uc?export=view&id=1tECJ0IccnLowaR1qK1zgNH4zLU3foA8V)

## External Libraries used
<ol>
<l1>
    Materialize CSS:
    <ul>
        <li>https://fonts.googleapis.com/icon?family=Material+Icons </li>
        <li>https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css </li>
        <li>https://code.jquery.com/jquery-2.1.1.min.js</li>
        <li>https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js</li>
    </ul>
</li>
<li>
    Django Channels
    <ul>
        <li>https://channels.readthedocs.io/en/latest/installation.html</li>
    </ul>
</li>
<li>
    redis
    <ul>
        <li><p>'windows installer msi' at</p> <p> https://github.com/MSOpenTech/redis/releases</p>
	Note: 
	1.set PATH variable.
	2. Reboot system after install.</li>
    </ul>
</li>
<li>pip install pypiwin32</li>
<li>pip install twisted</li>
</ol>

## How to Use?
<ol>
<li>
    For Email notification feature(and thus website to work properly)
    <ul>
    <li>In settings.py set EMAIL_HOST_USER as your GMAIL email and,</li>
    <li>set EMAIL_HOST_PASSWORD as your GMAIL password.</li>
    </ul>
</li>
<li>
    Register admin account.
</li>
    
<li>
    Add professors and students(They may swiftly be added from 'Django Site Administration' for testing purposes).
</li>
    
<li>
    Set default student password from admin account.
</li>
<li>
    Allot group leaders from admin account. Email notification will be sent to group leaders.
</li>
<li>
    Mentor assignment will be done in 3 rounds. In Every round and before first round, those group leaders who have not been allotted any mentor can fill preference from their account.
</li>
<li>
    Login from 'group leader account'(all leaders). Fill preferences for first round mentor assignment.
</li>
<li>
    Go to admin account and do 'Round 1 assignment'. Email notif will be sent to those leaders to whom mentor is allotted in round 1.
</li>
<li>
    Fill preferences for round 2 in those leader account whom mentors have not been allotted in round 1.
</li>
<li>
    Again go to admin and do 'Round 2 Assignment'.
</li>
<li>
Repeat above steps for Round 3.
</li>
<li>
Group Leaders can send invite to available students. Email notification will be sent to students.
</li>
<li>
Student can accept invite from student account. Email notif will be sent to that leader whose invitation has been accepted.
</li>
<li>
CHAT ROOM:
<ul>
<li> Enter same 'room name' to chat.</li>
<li> Chats are not saved in database. So chatting can be done between those who are online.
<li>Tell your name with message every time a message is sent in chat room.
</ul>
</li>
<li>
    Information about developers in Footer.
</li>
</ol>
