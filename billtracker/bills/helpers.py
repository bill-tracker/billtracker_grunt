import base64
import re
from bs4 import BeautifulSoup

def decode(encoded_string):
    return base64.b64decode(encoded_string)

def strip_html(html_string):
    bill_text = BeautifulSoup(html_string, 'html.parser')
    bill_text.find('style').extract()
    bill_text = bill_text.get_text().split('\n')
    bill_text = list(filter(lambda x: re.search('\w+', x), bill_text))
    bill_text = '\n'.join(bill_text)
    return bill_text.replace(u'\xa0', u' ')