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
    numbers = soup.find_all('a', class_="pag_link")
    number = numbers[-2].text
    
    return (int(number))

def get_petition_name(petition):
    html = get_html(BASE_URL+str(petition))
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').text
    return title

def parse(petition):
    signers = []
    pages = get_page_count(get_html(BASE_URL+str(petition)))
    for page in range(pages):        
        html = get_html(BASE_URL+petition+'/votes/'+str(page+1))
        soup = BeautifulSoup(html, 'html.parser')        
        for name in soup.find_all('div', class_="table_cell name"):        
            signers.append(name.text)
    
    return signers

def save_excel(signers, filename):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Підписанти')    
    #ws.write(0, 0, 'Ім\'я')
    
    for i in range(len(signers)):
        ws.write(i,0,signers[i])
    wb.save(filename+'.xls')

def save_scv(signers, filename):
    with open(filename+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        #writer.writerow(['Ім\'я'])

        for signer in signers:
            writer.writerow([signer])
def main():
    print('Parsing data... Please wait... It can take a few minutes...')
    title = get_petition_name(petition)[:110]
    signers = parse(petition)
    
    filename = title+' ('+petition+')'
    save_excel(signers, filename)
    
if __name__ == '__main__':
    if len(sys.argv)>1:
        petition = sys.argv[1]
    else:
        petition = str(input('Введіть номер петиціїї: '))
        
    main()
