import requests
import re
from requests.compat import quote_plus # put %20 and + between the spaces in the url
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/d/services/search/bbb?query={}&sort=rel'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    # print(quote_plus(search))

    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

    # webscraping part - extracting data from the website using BeautifulSoup
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        pre_post_title = post.find(class_='result-title').text
        if len(pre_post_title) > 40:
            post_title = pre_post_title[:40] + '...'
        else:
            post_title = pre_post_title
            

        post_url = post.find('a').get('href')

        if post.find(class_='result-date'):
            post_date = post.find(class_='result-date').text
        else:
            post_date = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_date, post_image_url))

    return render(request, 'my_app/new_search.html', {
        'search': search,
        'final_postings': final_postings
    })