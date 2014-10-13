#! /usr/bin/python
import requests
from bs4 import BeautifulSoup, NavigableString
import re

def get_review_in_sentences(book_url):
  
  #Get book review
  response = requests.get(book_url)
  soup = BeautifulSoup(response.text)
  review = soup.select('div.simple-html')[1]

  #Remove excess whitespace, tags, newlines 
  p = re.compile('(</?[a-zA-z]*/?>|\r|\s{2,}|\t)')
  review = [p.sub('', str(line)) for line in review]

  #Remove all non-letter character except for periods
  p = re.compile('[^\.\w]')
  review = [p.sub(' ', str(line)) for line in review]

  review = '.'.join(review)
  p = re.compile('\s+')
  review = p.sub(' ', review)
  sentences = review.split('.')
  print sentences





get_review_in_sentences('http://www.barnesandnoble.com/w/skin-game-jim-butcher/1115202091?ean=9780451464392')