from django.core.management.base import BaseCommand, CommandError
from bills.models import *
from bills.helpers import decode, strip_html

class Command(BaseCommand):
    help = 'Crawls database and decodes/parses bill'

    # def add_arguments(self, parser):

    def handle(self, *args, **options):
        documents = BillRevision.objects.all()
        for document in documents:
            print 'processing revision {0} for bill {1}...'.format(document.date, document.bill.number)
            document.raw_text = strip_html(decode(document.doc_encoded))
            document.save()