from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Bill
import requests
from bs4 import BeautifulSoup

def index(request):
    bills = Bill.objects.order_by('-date')
    return render(request, 'bills/index.html', {'bills':bills})

def about_us(request):
    return render(request, 'bills/about.html')

def bill_listing(request):
    return render(request, 'bills/bill-listing.html')

def blog(request):
    return render(request, 'bills/blog.html')

def contact_us(request):
    return render(request, 'bills/contact.html')

def single(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    return render(request, 'bills/single.html', {'bill':bill})

def search_by_title(request):
    bills = Bill.objects.order_by('-date')
    try:
        bill = bills.get(title=request.POST['Title'])
    except (KeyError, Bill.DoesNotExist):
        return render(request, 'bills/index.html', {
            'bills': bills,
            'error_message': "Bill not found in database.",
        })
    else:
        return HttpResponseRedirect(reverse('bills:index', args=(bill.id,)))

def scraper(request):
    scrape_response = requests.get('http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/HB00004I.htm')
    plain_text = scrape_response.text
    soup = BeautifulSoup(plain_text, 'html.parser').prettify()
    return render(request, 'bills/scraper.html', {'scrape_text':soup})
