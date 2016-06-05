from django.db import models
from django.utils import timezone

class Bill(models.Model):
    title = models.CharField(max_length=500, default="")
    text = models.CharField(max_length=1000000, default="")
    date = models.DateField(auto_now_add = True, editable=False)
    get_latest_by = 'date'
    def __str__(self):
        return self.title
