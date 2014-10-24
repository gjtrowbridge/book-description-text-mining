#! /usr/bin/python
import requests
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
import re
import json

driver = webdriver.Firefox()

def get_links_from_page(category_url):
  #Get all links
  # response = requests.get(category_url)
  driver.get(category_url)
  page_source = driver.page_source.encode('utf-8')

  f = open('link_data.html', 'w')
  f.write(page_source)
  f.close()

  soup = BeautifulSoup(page_source)
  links = soup.select('div#search-results-1 ol.result-set li.result div.display-tile-item div.details a.title')

  #Creates an array of objects containing data about the books
  books = []
  for link in links:
    book = {}
    book['url'] = link['href']
    c = link.contents[0]
    if (isinstance(c, NavigableString)):
      book['title'] = link.contents[0]
    else:
      book['title'] = c['title']
    books.append(book)
    print 'Added book: ' + book['title']

  return books

def add_book_descriptions(book):
  
  print 'Getting description for book: ' + book['title']

  #Get book review
  response = requests.get(book['url'])
  soup = BeautifulSoup(response.text)
  review = soup.select('div.simple-html')[1].prettify().encode('utf-8')
  book['raw_description'] = review

  sentences = re.split('\.|<p>', review)

  for i in range(len(sentences)):

    #Remove tags
    p = re.compile('</?([a-zA-z]|"|-|=|\s|\/)*>')
    sentences[i] = p.sub('', sentences[i])

    #Remove newlines, tabs
    p = re.compile('(\n|\t|\r)+')
    sentences[i] = p.sub(' ', sentences[i])

    #Remove all non-letter characters except periods
    p = re.compile('[^\.\w]')
    sentences[i] = p.sub(' ', sentences[i])

    #Remove all excess spaces
    p = re.compile('\s+')
    sentences[i] = p.sub(' ', sentences[i])

  book['sentences'] = sentences

  #Not used in this code, but returns book anyway
  return book

#Get all book links
books = get_links_from_page('http://www.barnesandnoble.com/s/?aud=tra&csrftoken=loWBCaA9KDjHBpXHkQRHZNHZHYuQ6xZ0&dref=51&fmt=physical&size=90&sort=SA&store=BOOK&view=grid')


# book = {}
# book['url'] = 'http://www.barnesandnoble.com/w/burned-karen-marie-moning/1118082011?ean=9780553390377'
# book['url'] = 'http://www.barnesandnoble.com/w/george-r-r-martins-a-game-of-thrones-5-book-boxed-set-martin-george-r-r/1117519253?ean=9780345535528'
# book['title'] = 'burned'
# add_book_descriptions(book)
# print book

#Get the book descriptions
# for book in books:
#   add_book_descriptions(book)

# #Output the books data to a text file
# f = open('book_data.txt', 'w')
# f.write(json.dumps(books))

driver.quit()
print 'Completed.'

