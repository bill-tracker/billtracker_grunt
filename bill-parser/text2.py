from bs4 import BeautifulSoup as bs4
import requests
import re

bill_request = requests.get('http://www.legis.state.tx.us/tlodocs/84R/billtext/html/HB00002I.htm')

bill_text = bill_request.text

# Preserve underlines (<u>) & strikethroughs (<s>)
for tag in ['u', 's']:
    bill_list = bill_text.split('</' + tag + '>')
    if len(bill_list) > 1:
        for i in range(len(bill_list)-1):
            bill_list[i] = bill_list[i].replace('<' + tag + '>', '¿' + tag + '¡')

        bill_text = ('¿/' + tag + '¡').join(bill_list)

bill_soup = bs4(bill_text, 'html.parser')

bill_soup.find('style').extract()

td_list = bill_soup.find_all('td', { 'width': '65' })

for td in td_list:
    td.extract()

bill_text = bill_soup.get_text().replace('\n', ' ')
# bill_text = bill_soup.get_text().split('\n')
#
# bill_text = list(filter(lambda x: re.search('\w+', x), bill_text))
#
# bill_text = ' '.join(bill_text)

# bill_text = str(bill_text.encode('ascii', 'replace'))

bill_text = re.sub(r' {2,}', ' ', bill_text)
# ' '.join(bill_text.split(' '))

# bill_text = ' '.join(bill_text.split('  '))


def section_repl(matchobj):
    try:
        return '\n\n' + matchobj.group(1) + 'S'
    except:
        return '\n\nS'

# print(re.search(r'\xa0{7}(¿/?[us]¡)S', bill_text).group(1))
bill_text = re.sub(r'\xa0{7}(¿/?[us]¡)?S', section_repl, bill_text)
# bill_text = bill_text.replace(('\xa0' * 7) + 'S', '\n\nS')
# bill_text = bill_text.split(('\xa0' * 7) + 'S')

# for i in range(len(bill_text)):
# # for paragraph in bill_text:
#     try:
#         def subsection_a_repl(matchobj):
#             return matchobj.group(1) + '.\n('
#
#         bill_text[i] = re.sub(r'(\..+[A-Z]+)(\. .?\()', subsection_a_repl, bill_text[i])
#         # print(re.search('(\..+[A-Z]+)(\. .?\()', bill_text[i]).group(2))
#     except:
#         pass

# bill_text = '\n\nS'.join(bill_text)


def subsection_repl(matchobj):
    return matchobj.group(1) + '.\n('

bill_text = re.sub(r'(\..+[A-Z]+)(\. .?\()', subsection_repl, bill_text)
# print(re.search('(\..+[A-Z]+)(\. .?\()', bill_text[i]).group(2))

def subsection_repl(matchobj):
    return matchobj.group(1) + '.\n('

# bill_text = re.sub(r'(\..+[A-Z]+)(\. .?\()', subsection_repl, bill_text[i])
# print(re.search(r'\xa0{7}(\xa0{6})?\(', bill_text).group())

bill_text = bill_text.replace(('\xa0' * 13) + '(', '\n(')
# bill_text = '\n('.join(bill_text.split(('\xa0' * 13) + '('))

bill_text = bill_text.replace(('\xa0' * 7) + '(', '\n(')

# bill_text = '\n('.join(bill_text.split(('\xa0' * 7) + '('))

# bill_text = '\n'.join(bill_text.split('\xa0\xa0\xa0\xa0\xa0\xa0\xa0'))

print(bill_text[:300])
