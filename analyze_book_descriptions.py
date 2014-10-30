#! /usr/bin/python

import json
import re
import copy
import math

def load_books(category):
  f = open(category + '_book_data.txt', 'r')
  return json.loads(f.read())
  f.close()

def add_word_counts(books, overall_word_counts={}, number_of_words=0):
  for book in books:
    book['word_counts'] = {}
    for sentence in book['sentences']:
      words = re.split(u'\s+', sentence)
      for word in words:
        if (len(word) <= 2):
          pass
        else:
          word = word.lower()
          number_of_words += 1
          if (word in book['word_counts']):
            book['word_counts'][word] += 1
          else:
            book['word_counts'][word] = 1

          if (word in overall_word_counts):
            overall_word_counts[word] += 1
          else:
            overall_word_counts[word] = 1
  return number_of_words

scifi_books = load_books('scifi')
humor_books = load_books('humor')
thriller_books = load_books('thriller')
fiction_literature_books = load_books('fiction_literature')

overall_word_counts = {}

#Get total # of words in Sci Fi descriptions
number_sci_fi_words = add_word_counts(scifi_books, overall_word_counts)

#Get dictionary of word counts in sci fi
scifi_word_counts = copy.deepcopy(overall_word_counts)

#Get total # words in other categories, sum up word counts for all categories
number_humor_words = add_word_counts(humor_books, overall_word_counts)
number_thriller_words = add_word_counts(thriller_books, overall_word_counts)
number_fiction_words = add_word_counts(fiction_literature_books, overall_word_counts)

#Get total # words for all categories
number_overall_words = number_sci_fi_words + number_humor_words + number_fiction_words + number_thriller_words

#Get list of scifi z-scores
scifi_z_scores = []

#Loop over all words in scifi list
for word in scifi_word_counts:
  if (word in overall_word_counts):
    #Get count for current word
    scifi_count = scifi_word_counts[word]
    #Get overall count for current word
    overall_count = overall_word_counts[word]
    #Convert overall count to be based on same # words as sci_fi count
    effective_overall_count = overall_count * 1.0 / number_overall_words * number_sci_fi_words
    #Get and save z-score
    z_score = (scifi_count - effective_overall_count) / math.sqrt(effective_overall_count)
    scifi_z_scores.append([z_score, word])

scifi_z_scores = sorted(scifi_z_scores, key=lambda tuple: tuple[0], reverse=True)
for i in range(50):
  [z_score, word] = scifi_z_scores[i]
  print word + '|' + str(z_score) + '|' + str(overall_word_counts[word]) + '|' + str(scifi_word_counts[word])
