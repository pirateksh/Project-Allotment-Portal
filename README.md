# Django_projects
<h3>External Libraries used:-</h3>
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

<h3>Instructions</h3>
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
