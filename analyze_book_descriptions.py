import json
import re
import copy

def load_books(category):
  f = open(category + '_book_data.txt', 'r')
  return json.loads(f.read())

def add_word_counts(books, overall_word_counts={}):
  for book in books:
    book['word_counts'] = {}
    for sentence in book['sentences']:
      words = re.split(u'\s+', sentence)
      for word in words:
        if (word == ''):
          pass
        else:
          word = word.lower()
          if (word in book['word_counts']):
            book['word_counts'][word] += 1
          else:
            book['word_counts'][word] = 1

          if (word in overall_word_counts):
            overall_word_counts[word] += 1
          else:
            overall_word_counts[word] = 1

scifi_books = load_books('scifi')
humor_books = load_books('humor')
thriller_books = load_books('thriller')
fiction_literature_books = load_books('fiction_literature')

overall_word_counts = {}
add_word_counts(scifi_books, overall_word_counts)

scifi_word_counts = copy.deepcopy(overall_word_counts)

add_word_counts(humor_books, overall_word_counts)
add_word_counts(thriller_books, overall_word_counts)
add_word_counts(fiction_literature_books, overall_word_counts)



print overall_word_counts['end']
