from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.template import RequestContext
from .models import *
import requests
import base64
import re
from bs4 import BeautifulSoup

def render_response(request, template, params = None):
    return render(request, template, params, context_instance=RequestContext(request))

def index(request):
    return render_response(request, 'bills/index.html')

def about_us(request):
    return render_response(request, 'bills/about.html')

def bill_listing(request):
    bills = Bill.objects.order_by('-last_action_date')[:100]
    return render_response(request, 'bills/bill-listing.html', { 'bills': bills })

def blog(request):
    return render_response(request, 'bills/blog.html')

def contact_us(request):
    return render_response(request, 'bills/contact.html')

def single(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    revisions = bill.billrevision_set.all()
    return render_response(request, 'bills/single.html', { 
        'bill': bill,
        'revisions': revisions
    })

def subsection_repl(matchobj):
    return matchobj.group(1) + '.\n('

def revision(request, bill_id, rev_id):
    print 'Fetching bill {0} revision {1}...'.format(bill_id, rev_id)
    revision = get_object_or_404(BillRevision, pk=rev_id)
    bill = get_object_or_404(Bill, pk=bill_id)

    decoded_text = base64.b64decode(revision.doc_encoded)
    bill_soup = BeautifulSoup(decoded_text, 'html.parser')
    bill_soup.find('style').extract()
    bill_text = bill_soup.get_text().split('\n')
    bill_text = list(filter(lambda x: re.search('\w+', x), bill_text))
    bill_text = ' '.join(bill_text)
    # bill_text = bill_text.split(('\xa0' * 7) + 'S')
    # bill_text = '\n\nS'.join(bill_text)
    # bill_text = re.sub(r'(\..+[A-Z]+)(\. .?\()', subsection_repl, bill_text)
    # bill_text = bill_text.replace(('\xa0' * 13) + '(', '\n(')
    # bill_text = bill_text.replace(('\xa0' * 7) + '(', '\n(')

    print bill_text

    return render_response(request, 'bills/revision.html', {
        'bill': bill,
        'revision': revision,
        'body': bill_text,
        'html': decoded_text
    })

def search_by_title(request):
    bills = Bill.objects.order_by('-last_action_date')
    try:
        bill = bills.get(title=request.POST['Title'])
    except (KeyError, Bill.DoesNotExist):
        return render_response(request, 'bills/index.html', {
            'bills': bills,
            'error_message': "Bill not found in database.",
        })
    else:
        return HttpResponseRedirect(reverse('bills:index', args=(bill.id,)))

def scraper(request):
    scrape_response = requests.get('http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/HB00004I.htm')
    plain_text = scrape_response.text
    soup = BeautifulSoup(plain_text, 'html.parser').prettify()
    return render_response(request, 'bills/scraper.html', {'scrape_text':soup})
