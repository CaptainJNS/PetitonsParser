import sys
import urllib.request
from bs4 import BeautifulSoup
import csv, xlwt

BASE_URL = 'https://petition.president.gov.ua/petition/'

def get_html(url):
    response = urllib.request.urlopen(url)
    
    return response.read()

def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    numbers = soup.find_all('a', class_ = 'pag_link')
    number = numbers[-2].text
    
    return (int(number))

def get_petition_name(petition_id):
    html = get_html(BASE_URL + str(petition_id))
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').text
    return f'{petition_id}. {title}'

def parse(petition_id):
    signers = []
    pages = get_page_count(get_html(BASE_URL + str(petition_id)))
    for page in range(pages):        
        html = get_html(BASE_URL + petition_id + '/votes/' + str(page + 1))
        soup = BeautifulSoup(html, 'html.parser')        
        for name in soup.find_all('div', class_ = 'table_cell name'):        
            signers.append(name.text)
    
    return signers

def save_excel(signers, filename):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Підписанти')    
    # ws.write(0, 0, 'Ім\'я') # header
    
    for i in range(len(signers)):
        ws.write(i, 0, signers[i])
    wb.save(filename + '.xls')

def save_scv(signers, filename):
    with open(filename + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['Ім\'я']) # header

        for signer in signers:
            writer.writerow([signer])

def main():
    print('Parsing data... Please wait... It can take a few minutes...')
    title = get_petition_name(petition_id)[:110]
    signers = parse(petition_id)
    
    save_excel(signers, title)
    save_scv(signers, title)
    print('Done.')
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        petition_id = sys.argv[1]
    else:
        petition_id = str(input('Введіть ID петиціїї: '))
        
    main()
