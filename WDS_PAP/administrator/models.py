from django.db import models

# Create your models here.


class Administrator(models.Model):
    username = models.CharField(verbose_name="Username", max_length=200)
    password = models.CharField(verbose_name="Hashed Password", max_length=500)
    is_stu_pass_set = models.BooleanField(verbose_name="Is student password set", default=False)
    is_lead_allotted = models.BooleanField(verbose_name="Are leaders allotted", default=False)
    round_1 = models.BooleanField(verbose_name="Round 1 allotment done", default=False)
    round_2 = models.BooleanField(verbose_name="Round 2 allotment done", default=False)
    round_3 = models.BooleanField(verbose_name="Round 3 allotment done", default=False)
    is_mentor_assigned = models.BooleanField(verbose_name="Is mentor assigned", default=False)

    def __str__(self):
        return self.username
