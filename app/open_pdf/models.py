from django.db import models


# Create your models here.


class PdfSchedule(models.Model):
    step = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    isSuccess = models.BooleanField(default=False)
    errors = models.TextField(default=None)
    dirName = models.CharField(max_length=140, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
