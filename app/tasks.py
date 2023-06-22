from urllib import request
from bs4 import BeautifulSoup
import random


# follow url to extract book title and description contents
def page_content(url):

    print(f'Extracting text: {url}')
    r = request.urlopen(url)
    soup = BeautifulSoup(r.read().decode(), "lxml")

    # soup extraction
    title = soup.find("title").text
    product_description = soup.find("div", {"id": "product_description"}).findNext("p").text

    # preprocess title
    title = title.strip().replace(' | Books to Scrape - Sandbox','')

    return title, product_description

# page with books listed
def book_page(url):
    print(f'Page url: {url}')
    r = request.urlopen(url)
    soup = BeautifulSoup(r.read().decode(), "lxml")

    # links to all books on page
    tags = soup.find_all("div", {"class": "image_container"})

    href_urls = []
    for tag in tags:
        href = tag.a['href']
        url = 'https://books.toscrape.com/catalogue/'+href
        href_urls.append(url)

    # randomly select 3 href_urls from list
    selected_urls = random.sample(href_urls, 3)

    # extract title, product_description from each href_url
    extracted_content = []
    for url_return in selected_urls:
        content = page_content(url_return)
        extracted_content.append(content)

    return extracted_content

