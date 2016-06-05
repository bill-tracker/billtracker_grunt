from django.core.management.base import BaseCommand, CommandError
from bills.models import *
from bills.services.legiscanService import LegiscanService
import requests
import sys

class Command(BaseCommand):
    help = 'Pulls sponsor and bill data from LegiScan'

    def add_arguments(self, parser):
        parser.add_argument('-a', '--all', action='store_true', dest='all',
            default=False, help='Syncs all entities from Legiscan'
        )
        parser.add_argument('-s', '--sessions', action='store_true', dest='sessions',
            default=False, help='Pulls missing sessions from Legiscan'
        )
        parser.add_argument('-b', '--bills', action='store_true', dest='bills',
            default=False, help='Pulls missing missing bills from Legiscan'
        )
        parser.add_argument('-r', '--revisions', action='store_true', dest='revisions',
            default=False, help='Pulls missing bill revisions from Legiscan'
        )
        parser.add_argument('-p', '--sponsors', action='store_true', dest='sponsors',
            default=False, help='Pulls missing bill revisions from Legiscan'
        )
        # parser.add_argument('-t', '--throttle', type=int,
        #     help='Throttles the number of requests to Legiscan'
        # )

    def handle(self, *args, **options):
        if options['all']:
            self.__syncSessions()
            self.__syncBills()
            self.__syncBillDetails()

        if options['sessions']: self.__syncSessions()
        if options['bills']: self.__syncBills()
        if options['revisions'] or options['sponsors']:
            self.__syncBillDetails(options['revisions'], options['sponsors'])

    def __syncSessions(self):
        self.__taskStart('Syncing sessions')

        sessionList = LegiscanService.getSessionList('TX')

        for session in sessionList['sessions']:
            if Session.objects.filter(id=session['session_id']).count() == 0:
                Session.create(session).save()
            self.__taskProgress()
        self.__taskEnd()

    def __syncBills(self):
        sessions = Session.objects.all()

        for session in sessions:
            self.__taskStart('Syncing bills for session {id} ({year_start} - {year_end})'.format(
                id=str(session.id), year_start=session.year_start, year_end=session.year_end))
            masterList = LegiscanService.getMasterList(session=session.id)

            for key, bill in masterList['masterlist'].iteritems():
                if 'bill_id' in bill and Bill.objects.filter(id=bill['bill_id']).count() == 0:
                    Bill.create(bill).save()
                self.__taskProgress()
            self.__taskEnd()

    def __syncBillDetails(self, revisions=False, sponsors=False):
        if not revisions and not sponsors: return

        bills = Bill.objects.all().order_by('-last_action_date')

        for bill in bills:
            print 'Fetching details for bill {0} ({1}):'.format(bill.number, bill.last_action_date)
            billDetails = LegiscanService.getBill(bill.id)
            if revisions: self.__syncBillRevisions(bill, billDetails)
            if sponsors: self.__syncBillSponsors(bill, billDetails)

    def __syncBillRevisions(self, bill, billDetails):
        self.__taskStart('Fetching revisions for {0}'.format(bill.number))
        revisions = billDetails['bill']['texts']
        for revision in revisions:
            rev_id = revision['doc_id']
            if BillRevision.objects.filter(id=rev_id).count() == 0:
                billRevisionData = LegiscanService.getBillRevision(rev_id)
                revision = billRevisionData['text']
                BillRevision.create(revision, bill).save()
            self.__taskProgress()
        self.__taskEnd()

    def __syncBillSponsors(self, bill, billDetails):
        self.__taskStart('Fetching sponsors for {0}'.format(bill.number))
        sponsors = billDetails['bill']['sponsors']
        for sponsor in sponsors:
            sponsor_id = sponsor['people_id']
            savedSponsor = Sponsor.objects.filter(id=sponsor_id).first()
            if savedSponsor is None:
                sponsorData = LegiscanService.getSponsor(sponsor_id)
                savedSponsor = Sponsor.create(sponsorData['person'])
                savedSponsor.save()
            savedSponsor.bills.add(bill)
            savedSponsor.save()
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










