from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd

s= HTMLSession()

url = "https://www.amazon.com/s?k=monitor"
def page(url,num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Path':f'/s?k=monitor&page={str(num)}&qid=1684865096&ref=sr_pg_{str(num)}',
    }

    r = s.get(url,headers=headers)
   
    print(r.status_code)
    print(r.request.headers)
    soup = BeautifulSoup(r.text,'lxml')
    return soup

def parse(soup):
    results = soup.find_all('div',{'data-component-type':'s-search-result'})

    products = []
    for x in results:
        try:
            product ={

                'title': x.find('span',{'class':'a-size-medium a-color-base a-text-normal'}).text,
                'price': x.find('div',{'class':'a-section a-spacing-none a-spacing-top-micro puis-price-instructions-style'}).find('span',{'class':'a-offscreen'}).text,
                }
            products.append(product)
        except:
            product ={
                'title': 'null',
                'price': 'null'
                }
            products.append(product)

    print(len(products))  
    return products    

def nextPage():
    page = soup.find('span',{'class':'s-pagination-strip'})
    if not page.find('span',{'class':'s-pagination-item s-pagination-next s-pagination-disabled '}):
        full_link = 'https://www.amazon.com' + str(page.find('a',{'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'}).get('href'))
        return full_link
    
    else:
        return
    
df = pd.DataFrame()
num = 0
while True:
    
    sum = 1
    num = num + sum 
    print(num)
    soup = page(url,num)
    products = parse(soup)
    f = pd.DataFrame(products)
    df = df._append(f)    
    url =nextPage()
    if url == None:
        break
    print(url)
   

    df.to_csv('products.csv')

