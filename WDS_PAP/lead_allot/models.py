from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(verbose_name='Name of Student', max_length=500)
    reg_no = models.CharField(verbose_name='Registration Number', max_length=256)
    branch = models.CharField(verbose_name='Branch', max_length=200)
    cpi = models.DecimalField(verbose_name='CPI', max_digits=4, decimal_places=2)
    email = models.EmailField(verbose_name='Email of Student', max_length=100, default='0')
    is_lead = models.BooleanField(verbose_name='Is Leader?', default=False)
    is_avail = models.BooleanField(verbose_name='Is Available?', default=True)
    password = models.CharField(verbose_name="Hashed Password", max_length=500, default='0')
    grp_no = models.IntegerField(verbose_name="Group No", default=0)
    invited_by = models.CharField(verbose_name="Invited by", max_length=200, default='0,')

    def __str__(self):
        return self.name


class Leader(models.Model):
    name = models.CharField(verbose_name='Name of Student', max_length=500)
    reg_no = models.CharField(verbose_name='Registration Number', max_length=256)
    email = models.EmailField(verbose_name='Email of Leader', max_length=100, default='0')
    rank = models.IntegerField(verbose_name="Rank", default=0)
    pref_1 = models.CharField(verbose_name='Preference 1', max_length=200, default='0')
    pref_2 = models.CharField(verbose_name='Preference 2', max_length=200, default='0')
    pref_3 = models.CharField(verbose_name='Preference 3', max_length=200, default='0')
    password = models.CharField(verbose_name="Hashed Password", max_length=500, default='0')
    pref_allotted = models.CharField(verbose_name="Allotted Professor", max_length=200, default='0')
    invited = models.CharField(verbose_name="Invitee", max_length=200, default='0,')
    accepted_by = models.CharField(verbose_name="Invite Acceptor", max_length=200, default='0,')
    has_filled_pref = models.BooleanField(verbose_name="Has filled preferences?", default=False)

    def __str__(self):
        return self.name
