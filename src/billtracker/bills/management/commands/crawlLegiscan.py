from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date
from bills.models import *
from bills.services.legiscanService import LegiscanService
import requests

class Command(BaseCommand):
    help = 'Pulls sponsor and bill data from LegiScan'

    def handle(self, *args, **options):
        print 'Resetting bills...'
        Bill.objects.all().delete()
        print 'Pulling master list...'
        masterList = LegiscanService.getMasterList('TX')

        for key, bill in masterList['masterlist'].iteritems():
            if 'bill_id' in bill:
                print 'Processing bill: ' + str(bill['bill_id'])
                newBill = Bill(id=bill['bill_id'], number=bill['number'], title=bill['title'],
                            description=bill['description'], url=bill['url'],
                            last_action=bill['last_action'], last_action_date=parse_date(bill['last_action_date']),
                            status=bill['status'],
                            status_date=parse_date(bill['status_date']) if bill['status_date'] is not None else None)
                newBill.save()