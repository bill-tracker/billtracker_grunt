from django.db import models
from django.utils.dateparse import parse_date
from django.utils import timezone

class Session(models.Model):

    name = models.CharField(max_length=500, default="")
    session_name = models.CharField(max_length=500, default="")
    special = models.BooleanField()
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    state_id = models.IntegerField()

    created = models.DateField(auto_now_add = True, editable=False)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, session):
        return cls(id=session['session_id'], name=session['name'],
            session_name=session['session_name'], special=session['special'] == True,
            year_start=session['year_start'], year_end=session['year_end'],
            state_id=session['state_id'])

class Bill(models.Model):
    number = models.CharField(max_length=500, default="")
    title = models.CharField(max_length=500, default="")
    description = models.TextField(default="")

    last_action_date = models.DateField(null=False)
    last_action = models.CharField(max_length=500, null=True)

    status_date = models.DateField(null=True)
    status = models.CharField(max_length=500, null=True)

    url = models.CharField(max_length=500, null=True)

    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    created = models.DateField(auto_now_add = True, editable=False)

    def __str__(self):
        return self.title

    @classmethod
    def create(cls, name, email):
        return cls(id=bill['bill_id'], number=bill['number'], title=bill['title'],
            description=bill['description'], url=bill['url'],
            last_action=bill['last_action'], last_action_date=parse_date(bill['last_action_date']),
            status=bill['status'], session=session,
            status_date=parse_date(bill['status_date']) if bill['status_date'] is not None else None)

class BillRevision(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    date = models.DateField()
    doc_type = models.CharField(max_length=50, default="")
    doc_mime = models.CharField(max_length=50, default="")
    doc_encoded = models.TextField(default="")

    created = models.DateField(auto_now_add = True, editable=False)

    @classmethod
    def create(cls, revision, bill):
        return cls(id=revision['doc_id'], bill=bill,
            date=parse_date(revision['date']), doc_type=revision['type'],
            doc_mime=revision['mime'], doc_encoded=revision['doc'])


class Sponsor(models.Model):
    party_id = models.CharField(max_length=1, default="")
    party = models.CharField(max_length=1, default="")
    role = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=50, default="")
    first_name = models.CharField(max_length=50, default="")
    middle_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    district = models.CharField(max_length=25, default="")
    follow_the_money_id = models.CharField(max_length=10, default="")

    committee_sponsor = models.IntegerField()
    committee_id = models.IntegerField()

    suffix = models.CharField(max_length=50, default="")
    nickname = models.CharField(max_length=25, default="")

    bills = models.ManyToManyField(Bill)

    created = models.DateField(auto_now_add = True, editable=False)

    def __str__(self):
        return self.party + ' ' + self.name

    @classmethod
    def create(cls, sponsor):
        return cls(id=sponsor['people_id'], party_id=sponsor['party_id'], party=sponsor['party'],
            role=sponsor['role'], name=sponsor['name'], first_name=sponsor['first_name'],
            middle_name=sponsor['middle_name'], last_name=sponsor['last_name'], district=sponsor['district'],
            follow_the_money_id=sponsor['ftm_eid'], committee_id=sponsor['committee_id'], committee_sponsor=sponsor['committee_sponsor'],
            nickname=sponsor['nickname'], suffix=sponsor['suffix'])