import csv
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from bs4 import ResultSet

HOST = 'https://www.kivano.kg'
HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

def get_html(url: str, category: str, headers: dict='', params: str=''):
    html = requests.get(
        url + '/f/' + category,
        headers=headers,
        params=params,
        verify=False
    )
    return html.text


def get_cards(html: str) -> ResultSet:
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('div', class_='item product_listbox oh')
    return cards

def parse_data_from_cards(cards: ResultSet) -> list:
    result = []
    for card in cards:
        try:
            image_link = card.find('div', class_='listbox_img pull-left').find('img').get('src')
        except AttributeError:
            image_link = 'Нет картинки'
        try:
            in_stock = card.find('div', class_='listbox_motive text-center').find('span', style='color:#448511;').text
        except AttributeError:
            in_stock = 'Нет в наличии'
        obj = {
            'title': card.find('div', class_='listbox_title oh').find('strong').get('target'),
            'price': card.find('div', class_='listbox_price text-cente').get('strong') or 'Нет в наличии',
            'image_link': image_link,
            'card_link': HOST + card.find('div', class_='listbox_img pull-left').find('a').get('href'),
            'in_stock': in_stock
        }
        result.append(obj)
    return result


def write_to_csv(data: list, file_name):
    fieldnames = data[0].key()
    with open(f'{file_name}.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)



html = get_html(HOST, 'mobilnye-telefony')
# print(html)
cards = get_cards(html)
# print(cards)
data = parse_data_from_cards(cards)
print(data)
# # write_to_csv(data, 'mobilnye-telefony')
