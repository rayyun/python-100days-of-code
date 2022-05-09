# Day92-Professional Portfolio Project 12 : Custom Web Scraper

from bs4 import BeautifulSoup
import requests
import csv

SOURCE_URL = "https://www.allrecipes.com/"
FIELD_NAMES = ['title', 'url', 'category', 'rating', 'rating_count', 'meta_data', 'image_url',
               'ingredients', 'directions', 'nutrition']

CSV_FILE = 'recipe_list.csv'

recipe_list = []

# scrap category url
def get_category(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    categories = soup.find_all('a', class_='carouselNav__link')

    category_dict = {}

    for category in categories:
        # print(category.get('data-tracking-content-headline'))
        # print(category.get('href'))
        category_dict[category.get('data-tracking-content-headline')] = category.get('href')

    return category_dict


# scrap the recipe list
def scrap_recipe_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    recipe_urls = []

    items_link = soup.find_all('a', class_='card__titleLink')

    for item in items_link[::2]:
        recipe_urls.append((item.get('title'), item.get('href')))

    return recipe_urls


# scrape the recipe detail
def recipe_detail(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    print(url)

    # recipe category
    categories = soup.find(class_='breadcrumbs__list')
    category = categories.get_text().strip().split('  ')

    # recipe title
    title_tag = soup.find(class_='headline')
    if title_tag:
        title = title_tag.contents[0]
        # print(title_tag)
    else:
        make_recipe_list(scrap_recipe_urls(url))
        return


    # recipe rating
    rating_tag = soup.find(class_='review-star-text')
    rating = rating_tag.contents[0].split()[1] if rating_tag else None

    # recipe rating count
    rating_count_tag = soup.find(class_='ratings-count')
    rating_count = rating_count_tag.contents[0].split()[0] if rating_count_tag else None

    # recipe meta info
    meta_items_tag = soup.find(class_='recipe-meta-container')
    if meta_items_tag:
        meta_item = meta_items_tag.get_text().strip().split('   ')
        meta_item = [item.strip() for item in meta_item]
    else:
        meta_item = None

    # # recipe video link / image url  --> remove! many recipes don't have video
    # video_link = soup.find('video')
    # if video_link:
    #     video_json = json.loads(video_link.get('data-metadata'))
    #     video_url = video_json['brightcove']['sources'][4]['src']
    #     # image_url = video_link.get('poster')
    # else:
    #     video_url = None

    # recipe image url
    image_link = soup.find('button', class_='elementButton__defaultFocus')
    if image_link:
        image_url = image_link.get('data-image')

        # print('\t', video_url)
        print('\t', image_url)
    else:
        return


    # recipe ingredients
    ingredients_tag = soup.find_all(class_='ingredients-item-name')
    ingredients = []

    for ing in ingredients_tag:
        ingredients.append(ing.contents[0])

    # recipe directions
    directions_tag = soup.find_all(class_='paragraph')
    directions = []

    for dir in directions_tag:
        directions.append(dir.contents[0].get_text())

    # recipe nutrition
    nutrition_section = soup.find(class_='recipe-nutrition-section')
    nutrition = nutrition_section.get_text().strip() if nutrition_section else None

    recipe_info = {
        'title': title,
        'url': url,
        'category': category,
        'rating': rating,
        'rating_count': rating_count,
        'meta_data': meta_item,
        'image_url': image_url,
        'ingredients': ingredients,
        'directions': directions,
        'nutrition': nutrition
    }

    recipe_list.append(recipe_info)


def make_recipe_list(url_list):
    global recipe_list

    for title, url in url_list:
        recipe_detail(url)

    save_to_csv(recipe_list)
    recipe_list = []


def save_to_csv(item_list):
    with open(CSV_FILE, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        # writer.writeheader()
        writer.writerows(item_list)


category = get_category(SOURCE_URL)

for c_name, c_url in category.items():
    recipe_url = scrap_recipe_urls(c_url)

    make_recipe_list(recipe_url)
