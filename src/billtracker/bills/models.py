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

class BillRevision(models.Model):
    doc_id = models.IntegerField()
    bill_id = models.IntegerField()
    date = models.DateField()
    doc_type = models.CharField(max_length=50, default="")
    doc_mime = models.CharField(max_length=50, default="")
    doc_encoded = models.TextField(default="")

class Session(models.Model):
    name = models.CharField(max_length=500, default="")
    session_name = models.CharField(max_length=500, default="")
    special = models.BooleanField()
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    state_id = models.IntegerField()

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    party_id = models.CharField(max_length=1, default="")
    party = models.CharField(max_length=1, default="")
    role = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=10, default="")
    first_name = models.CharField(max_length=10, default="")
    middle_name = models.CharField(max_length=10, default="")
    last_name = models.CharField(max_length=10, default="")
    district = models.CharField(max_length=10, default="")
    follow_the_money_id = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.name