#! /usr/bin/python
import requests

def save_page(url, location):
  #Get all links
  response = requests.get(url)

  f = open(location, 'w')
  f.write(response.text)
  f.close()

save_page('http://www.readersread.com/excerpts', 'html/home_page.html')
