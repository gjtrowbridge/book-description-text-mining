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
      book['title'] =  c.encode('ascii', 'ignore')
    else:
      print type(c)
      book['title'] = c['title'].encode('ascii', 'ignore')
    books.append(book)

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
# mystery_crime_thriller_books = get_links_from_page('http://www.barnesandnoble.com/s/?csrfToken=xTH3wHNOE5hpZzyrhoMA4atLjUZr3LiB&sort=SA&size=90&aud=tra&csrftoken=loWBCaA9KDjHBpXHkQRHZNHZHYuQ6xZ0&dref=50&fmt=physical&store=BOOK&view=grid')
# scifi_fantasy_books = get_links_from_page('http://www.barnesandnoble.com/s/?csrfToken=aOYdQXwMSsh20t51PWAxuFMK2ZdX0DnK&sort=SA&size=90&aud=tra&csrftoken=loWBCaA9KDjHBpXHkQRHZNHZHYuQ6xZ0&dref=51&fmt=physical&store=BOOK&view=grid')

def get_book_descriptions(url, category):
  books = get_links_from_page(url)

  #Get the book descriptions
  for book in books:
    add_book_descriptions(book)
  
  f = open(category + '_book_data.txt', 'w')
  f.write(json.dumps(books))
  f.close()

get_book_descriptions('http://www.barnesandnoble.com/s/?csrfToken=xZxbp584k6gmsFaSq0zh0obG8I7sx9nz&sort=SA&size=90&aud=tra&dref=42&fmt=physical&store=BOOK&view=grid', 'humor')
get_book_descriptions('http://www.barnesandnoble.com/s/?csrfToken=xZxbp584k6gmsFaSq0zh0obG8I7sx9nz&sort=SA&size=90&aud=tra&csrftoken=xZxbp584k6gmsFaSq0zh0obG8I7sx9nz&dref=9&fmt=physical&store=BOOK&view=grid', 'fiction_literature')

driver.quit()
print 'Completed.'

