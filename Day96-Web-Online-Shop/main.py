# Day96-Professional Portfolio Project 16 : Online Shop

from bs4 import BeautifulSoup
import bs4
import requests
import tinycss




BASE_URL = "https://www.leonandgeorge.com"


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


categories = soup.find_all('div', class_='item')
print(len(categories))

for category in categories[1:]:
    # print(category.contents[1])

    ##### item name, item_url(for scrap details), item size
    item_name = category.contents[1].find('h6', class_='title').contents[0]
    item_url = BASE_URL + str(category.contents[1].get('href'))
    item_size = category.contents[1].select('a > p:nth-child(4)')[0].text
    ## Selector-path : #product-list > section > div > div > div > div:nth-child(73) > div > a > p:nth-child(4)

    # print(item_size)

    ############ price
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


    # print(item_name, price)
    price = int(price.replace('$', ''))



    ########## image url - small, med, large
    css = (category.contents[1].find('style'))

    # print(type(css.string))

    stylesheet = tinycss.make_parser().parse_stylesheet(css.string)
    # print(str(stylesheet.rules[0].declarations[0]).split())

    image_small = str(stylesheet.rules[0].declarations[0]).split()[3].replace('url(', '').replace('w=340)>', 'w=190')
    image_medium = str(stylesheet.rules[0].declarations[0]).split()[3].replace('url(', '').replace('w=340)>', 'w=380')
    image_large = str(stylesheet.rules[0].declarations[0]).split()[3].replace('url(', '').replace('w=340)>', 'w=480')

    # print('------------------')
    # print(image_small)
    # print(image_medium)
    # print(image_large)
    # print('------------------')

