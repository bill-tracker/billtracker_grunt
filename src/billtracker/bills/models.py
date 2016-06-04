from django.db import models
from django.utils import timezone

class Bill(models.Model):
    number = models.CharField(max_length=500, default="")
    title = models.CharField(max_length=500, default="")
    description = models.TextField(default="")

    last_action_date = models.DateField(null=True)
    last_action = models.CharField(max_length=500, null=True)

    status_date = models.DateField(null=True)
    status = models.CharField(max_length=500, null=True)

    url = models.CharField(max_length=500, null=True)

    date = models.DateField(auto_now_add = True, editable=False)
    get_latest_by = 'date'

    def __str__(self):
        return self.title
