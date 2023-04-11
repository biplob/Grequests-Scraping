import pandas as pd
from bs4 import BeautifulSoup
import grequests


def get_urls():
    urls = []
    for i in range(1,5):
      urls.append( f'https://www.canoeandkayakstore.co.uk/collections/boats-canoe-canoes?page={i}')

    return urls


def get_data(urls):

    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return  resp



def parse(resp):
    product_list = []
    for r in resp:
        sp = BeautifulSoup(r.text, 'html.parser')
        items = sp.find_all('div', {'class': 'product-grid-item__info'})

        for item in items:
            title = item.find_all('a')[0].text.strip()
            price = item.find('span', {'class': 'product-grid-item-price'}).find_all('span')[0].text.strip()
            availible = item.find('span', {'class': 'product-grid-item__info__availability--value'}).text.strip()


            product = {
                'title': title,
                'price': price,
                'available': availible,

            }
            product_list.append(product)
    return product_list





urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse(resp))
df.to_csv('canoes.csv', index=False)


