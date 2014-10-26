import json

f = open('book_data.txt', 'r')
books = json.loads(f.read())
print len(books)