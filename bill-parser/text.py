from bs4 import BeautifulSoup as bs4
import requests
import re

bill_request = requests.get('http://www.legis.state.tx.us/tlodocs/84R/billtext/html/HB00004I.htm')

bill_soup = bs4(bill_request.text, 'html.parser')

bill_soup.find('style').extract()

bill_text = bill_soup.get_text().split('\n')

bill_text = list(filter(lambda x: re.search('\w+', x), bill_text))

bill_text = ' '.join(bill_text)

# bill_text = str(bill_text.encode('ascii', 'replace'))

# ' '.join(bill_text.split(' '))

bill_text = ' '.join(bill_text.split('  '))


# bill_text = bill_text.replace(('\xa0' * 7) + 'S', '\n\nS')
bill_text = bill_text.split(('\xa0' * 7) + 'S')

# TODO: Speed test
# for i in range(len(bill_text)):
# # for paragraph in bill_text:
#     try:
#         def subsection_repl(matchobj):
#             return matchobj.group(1) + '.\n('
#
#         bill_text[i] = re.sub(r'(\..+[A-Z]+)(\. .?\()', subsection_repl, bill_text[i])
#         # print(re.search('(\..+[A-Z]+)(\. .?\()', bill_text[i]).group(2))
#     except:
#         pass

bill_text = '\n\nS'.join(bill_text)

# TODO: Speed test
def subsection_repl(matchobj):
    return matchobj.group(1) + '.\n('

bill_text = re.sub(r'(\..+[A-Z]+)(\. .?\()', subsection_repl, bill_text)
# print(re.search('(\..+[A-Z]+)(\. .?\()', bill_text[i]).group(2))


bill_text = bill_text.replace(('\xa0' * 13) + '(', '\n(')
# bill_text = '\n('.join(bill_text.split(('\xa0' * 13) + '('))

bill_text = bill_text.replace(('\xa0' * 7) + '(', '\n(')

# bill_text = '\n('.join(bill_text.split(('\xa0' * 7) + '('))

# bill_text = '\n'.join(bill_text.split('\xa0\xa0\xa0\xa0\xa0\xa0\xa0'))

print(bill_text)
