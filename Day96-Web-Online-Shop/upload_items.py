from bs4 import BeautifulSoup
import bs4
import requests
from datetime import date
import csv
import cssutils
import tinycss
from tinycss.css21 import CSS21Parser

BASE_URL = "https://www.leonandgeorge.com"

def get_today():
    return date.today().strftime("%m-%d-%Y %H:%M:%S")


# Upload bulk items at once (from web scraping data)
def bulk_upload(db, table_name):
    # url = "https://www.leonandgeorge.com/products/collection/all-plants"
    #
    # response = requests.get(url)

    # with open('test.html', 'w') as file:
    #     file.write(response.text)
    # print(response.text)


    with open('test.html', 'r') as file:
        html_file = file.read()

    # print(html_file)
    soup = BeautifulSoup(html_file, 'html.parser')

    # href link
    categories = soup.find_all('div', class_='item')
    print(len(categories) - 1)  # don't need first-row

    print(f'(before) [{table_name.__tablename__}] Table - {db.session.query(table_name.id).count()}')

    for category in categories[1:]:

        ############ price
        item_name = category.contents[1].find('h6', class_='title').contents[0]
        if str(item_name).strip() == 'Gift Card':
            continue

        prices = category.contents[1].find('p', class_='price').contents
        # print(prices)

        if len(prices) > 1:
            # print(type(prices[0]))
            if type(prices[0]) == bs4.element.Tag:
                price = prices[1].strip()
            else:
                price = prices[0].strip()
        else:
            price = prices[0].strip()

        price = int(price.replace('$', ''))


        # print(item_name, price)
        # price = int(price.replace('$', ''))

        ##### item name, item_url(for scrap details), item size
        # item_name = category.contents[1].find('h6', class_='title').contents[0]
        item_url = BASE_URL + str(category.contents[1].get('href'))
        item_size = category.contents[1].select('a > p:nth-child(4)')[0].text
        # item_size = category.contents[1].select('a > p:nth-child(4)')[0]
        # print(item_size)
        # print(item_url)
        # print(item_size)

        # product-list > section > div > div > div > div:nth-child(69) > div > a > p:nth-child(4)

        ########## image url (for list)
        css = (category.contents[1].find('style'))

        # print(type(css.string))

        stylesheet = tinycss.make_parser().parse_stylesheet(css.string)
        # print(str(stylesheet.rules[0].declarations[0]).split())

        image_sm_url = str(stylesheet.rules[0].declarations[0]).split()[3].replace('url(', '').replace('w=340)>', 'w=250') + '&h=330'
        image_md_url = str(stylesheet.rules[0].declarations[0]).split()[3].replace('url(', '').replace('w=340)>', 'w=380')
        image_lg_url = str(stylesheet.rules[0].declarations[0]).split()[3].replace('url(', '').replace('w=340)>', 'w=480')

        # print('------------------')
        # print(image_list)
        # print(image_detail)
        # print(image_enlarge)
        # print('------------------')

        print(item_url)

        # product detail (short / long)
        response_detail = requests.get(item_url)
        print(response_detail.status_code)
        # print(response_detail.text)
        soup_detail = BeautifulSoup(response_detail.text, 'html.parser')
        # print(soup_detail.text)

        short_detail = soup_detail.find('div', class_='product__entry').text.strip()
        # short_detail = soup_detail.find('div', class_='product__entry')
        # print(short_detail)

        long_detail = soup_detail.find('div', class_='section__body').text.strip()
        # long_detail = soup_detail.find('div', class_='section__body')
        # print(long_detail)

        # today_date = date.today().strftime("%m-%d-%Y %H:%M:%S")
        # today_date = get_today()

        new_item = table_name(
            name=item_name,
            size=item_size,
            quantity=10,
            price=price,
            discount=0,
            short_detail=short_detail,
            long_detail=long_detail,
            img_sm_url=image_sm_url,
            img_md_url=image_md_url,
            img_lg_url=image_lg_url,
            org_item_url=item_url,
            shop='T',
            createdAt=get_today(),
            updatedAt=get_today(),
            publishedAt=get_today()
        )

        db.session.add(new_item)
        db.session.commit()

    print(f'(after) [{table_name.__tablename__}] Table - {db.session.query(table_name.id).count()}')
