from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_date
from bills.models import *
from bills.services.legiscanService import LegiscanService
import requests
import sys

class Command(BaseCommand):
    help = 'Pulls sponsor and bill data from LegiScan'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--sessions', action='store_true', dest='sessions',
            default=False, help='Pulls missing sessions from Legiscan'
        )
        parser.add_argument('-b', '--bills', action='store_true', dest='bills',
            default=False, help='Pulls missing missing bills from Legiscan'
        )
        parser.add_argument('-r', '--revisions', action='store_true', dest='revisions',
            default=False, help='Pulls missing bill revisions from Legiscan'
        )
        parser.add_argument('-t', '--throttle', type=int,
            help='Throttles the number of requests to Legiscan'
        )

    def handle(self, *args, **options):
        if options['sessions']: self.__syncSessions()
        if options['bills']: self.__syncBills()
        if options['revisions']: self.__syncBillDetails()

    # def __truncateTables(self):
    #     print 'Truncating sessions...'
    #     Session.objects.all().delete()
    #     print 'Truncating bills...'
    #     Bill.objects.all().delete()

    def __syncSessions(self):
        self.__taskStart('Syncing sessions')

        sessionList = LegiscanService.getSessionList('TX')

        for session in sessionList['sessions']:
            session_id = session['session_id']
            if Session.objects.filter(id=session_id).count() == 0:
                Session(id=session_id, name=session['name'],
                    session_name=session['session_name'], special=session['special'] == True,
                    year_start=session['year_start'], year_end=session['year_end'],
                    state_id=session['state_id']).save()
            self.__taskProgress()
        self.__taskEnd()

    def __syncBills(self):
        sessions = Session.objects.all()

        for session in sessions:
            self.__taskStart('Syncing bills for session {id} ({year_start} - {year_end})'.format(
                id=str(session.id), year_start=session.year_start, year_end=session.year_end))
            masterList = LegiscanService.getMasterList(session=session.id)

            for key, bill in masterList['masterlist'].iteritems():
                if 'bill_id' in bill:
                    bill_id = bill['bill_id']
                    if Bill.objects.filter(id=bill_id).count() == 0:
                        Bill(id=bill_id, number=bill['number'], title=bill['title'],
                            description=bill['description'], url=bill['url'],
                            last_action=bill['last_action'], last_action_date=parse_date(bill['last_action_date']),
                            status=bill['status'], session=session,
                            status_date=parse_date(bill['status_date']) if bill['status_date'] is not None else None).save()
                    self.__taskProgress()
            self.__taskEnd()

    def __syncBillDetails(self, limit=None):
        document_download_count = 0
        bills = Bill.objects.all().order_by('-last_action_date')

        for bill in bills:
            self.__taskStart('Fetching details for bill {0} ({1})'.format(bill.number, bill.last_action_date))
            billDetails = LegiscanService.getBill(bill.id)
            revisions = billDetails['bill']['texts']

            for revision in revisions:
                rev_id = revision['doc_id']
                if BillRevision.objects.filter(id=rev_id).count() == 0:
                    billRevisionData = LegiscanService.getBillRevision(rev_id)
                    revision = billRevisionData['text']
                    BillRevision(id=revision['doc_id'], bill=bill,
                        date=parse_date(revision['date']), doc_type=revision['type'],
                        doc_mime=revision['mime'], doc_encoded=revision['doc']).save()
                    self.__taskProgress()
            self.__taskEnd()

    def __taskStart(self, task):
        print task,
        sys.stdout.flush()

    def __taskProgress(self):
        print '\b.',
        sys.stdout.flush()

    def __taskEnd(self):
        print 'Done!'










