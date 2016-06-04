from django.core.management.base import BaseCommand, CommandError
from bills.models import *
import requests

class Command(BaseCommand):
    help = 'Pulls sponsor and bill data from LegiScan'

    def handle(self, *args, **options):
        print 'Hello! You\'ve set me up correctly!'
        print Bill.objects.all()