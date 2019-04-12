from django.db import models

# Create your models here.


class Professor(models.Model):
    name = models.CharField(verbose_name="Name of Professor", max_length=200)
    dept = models.CharField(verbose_name="Department", max_length=200)
    aoi = models.CharField(verbose_name="Area of Interest", max_length=1000)
    email = models.EmailField(verbose_name="Email of Professor", max_length=100)
    nog = models.IntegerField(verbose_name="No of Groups")
    nog_assigned = models.IntegerField(verbose_name="No. of groups assigned", default=0)
    groups_assigned = models.CharField(verbose_name="Groups Assigned", max_length=200, default='0,')
    is_free = models.BooleanField(verbose_name="Is free", default=True)

    def __str__(self):
        return self.name
