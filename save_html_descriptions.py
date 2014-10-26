import json

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

save_to_html('scifi')
save_to_html('fiction_literature')
save_to_html('humor')
save_to_html('thriller')