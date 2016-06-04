from django.core.management.base import BaseCommand, CommandError
from bills.models import *
from bills.services.legiscanService import LegiscanService
import requests

class Command(BaseCommand):
    help = 'Pulls sponsor and bill data from LegiScan'

    def handle(self, *args, **options):
        print 'Pulling master list...'
        print LegiscanService.getMasterList('TX')