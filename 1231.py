import bs4
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re

r = input()
price_from = input("введи минимальную цену")
price_to = input("введи максимальную цену")
fbl = input("введи fbl")

session = requests.Session()

link = "https://member.expireddomains.net/login/"

a = UserAgent()
ua = a.random

data = {
    'login': 'sdfghdsfg',
    'password': 'esthermontgomery52260222@gmail.com'
}

headers = {
    'User-Agent': ua
}

responce = session.post(link, data=data, headers = headers).text
responce = session.get(f'https://member.expireddomains.net/domain-name-search/?start=0&fbl={fbl}&q={r}&fpricefrom={price_from}&fpriceto={price_to}#listing', headers = headers).text
soup = bs4.BeautifulSoup(responce, 'html.parser')
pages = soup.find('div',class_='pageinfo').text
pages = (int(re.sub(r'[\s+]', '',pages).replace("|", '').replace(",", '')[7:]))*25

x=0
while x <= pages:
    responce = session.get(f'https://member.expireddomains.net/domain-name-search/?start={x}&fbl={fbl}&q={r}&fpricefrom={price_from}&fpriceto={price_to}#listing', headers = headers).text
    soup = bs4.BeautifulSoup(responce, 'html.parser')
    test = soup.find_all("td", class_= 'field_domain')
    divs = re.findall(r'title=[\'\"](.+?)[\'\"]', str(test))
    i=0
    while i < len(divs):
        if divs[i] == 'Register at Namecheap.com' or divs[i] == 'Register at GoDaddy.com':
            del divs[i]
        else:
            i+=1
    x+=25
    domains = "\n".join(divs)
    print(divs)
    try:
        file_dom = open('domains.txt', 'a')
        file_dom.write(domains)
        file_dom.close()
    except:
        print('ошибка записи файла')
line_count = sum(1 for line in open('domains.txt'))
open_file = open('domains.txt', 'r')
j=1
for j in range(line_count):
    if j < line_count-1:
        dom = str(open_file.readlines(1))[2:-4]
        print(dom)
        resault = requests.get(f'https://api.similarweb.com/v1/similar-rank/{dom}/rank?api_key=550c7c3ed47b463c88f60aab76f24edd').text
        if resault!= '{"meta":{"status":"Error","error_code":401,"error_message":"Data not found"}}':
            resault = int(resault[resault.find('similar_rank":{"rank":')+22:-2])
            print(resault)
            fil = open('final_resault.txt', 'a')
            fil.write(f'{str(resault)} {dom}\n')
            fil.close()
        else:
            print('домен говно')
        j += 1
    else:
        dom = str(open_file.readlines(1))[2:-2]
        print(dom)
        resault = requests.get(f'https://api.similarweb.com/v1/similar-rank/{dom}/rank?api_key=550c7c3ed47b463c88f60aab76f24edd').text
        if resault != '{"meta":{"status":"Error","error_code":401,"error_message":"Data not found"}}':
            resault = int(resault[resault.find('similar_rank":{"rank":') + 22:-2])
            print(resault)
            fil = open('final_resault.txt', 'a')
            fil.write(str(resault) + dom)
            fil.close()
        else:
            print('домен говно')