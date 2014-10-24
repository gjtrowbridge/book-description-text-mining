#! /usr/bin/python
import requests
from bs4 import BeautifulSoup, NavigableString
import re
import json

def get_links_from_page(category_url):
  #Get all links
  response = requests.get(category_url)
  soup = BeautifulSoup(response.text)
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
  review = soup.select('div.simple-html')[1]
  book['raw_description'] = review

  #Remove excess whitespace, tags, newlines 
  p = re.compile('(</?[a-zA-z]*/?>|\r|\s{2,}|\t)')
  review = [p.sub('', str(line)) for line in review]

  #Remove all non-letter character except for periods
  p = re.compile('[^\.\w]')
  review = [p.sub(' ', str(line)) for line in review]

  review = '.'.join(review)
  p = re.compile('\s+')
  review = p.sub(' ', review)
  book['sentences'] = review.split('.')

  #Not necessary, but there if needed
  return book

#Get all book links
books = get_links_from_page('http://www.barnesandnoble.com/s/?aud=tra&csrftoken=loWBCaA9KDjHBpXHkQRHZNHZHYuQ6xZ0&dref=51&fmt=physical&size=90&sort=SA&store=BOOK&view=grid')

#Get the book descriptions
for book in books:
  add_book_descriptions(book)

#Output the books data to a text file
f = open('book_data.txt', 'w')
f.write(json.dumps(books))