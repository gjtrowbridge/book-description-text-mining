import json
import re

def load_books(category):
  f = open(category + '_book_data.txt', 'r')
  return json.loads(f.read())
  f.close()

def save_to_html(category):
  i = 1
  books = load_books(category)
  for book in books:
    f = open(category + '/file' + str(i) + '.html', 'w')
    f.write(book['raw_description'].encode('ascii', 'ignore'))
    f.close()
    i += 1

def save_to_text(category):
  p = re.compile('</?([a-zA-z]|"|-|=|\s|\/)*>')
  i = 1
  books = load_books(category)
  for book in books:
    f = open(category + '/file' + str(i) + '.txt', 'w')
    desc_no_tags = p.sub('', book['raw_description'])
    f.write(desc_no_tags.encode('ascii', 'ignore'))
    f.close()
    i += 1

save_to_text('scifi')
save_to_text('fiction_literature')
save_to_text('humor')
save_to_text('thriller')