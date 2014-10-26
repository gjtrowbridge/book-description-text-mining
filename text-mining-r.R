library(tm)
library(SnowballC)
library(RColorBrewer)
library(ggplot2)
library(magrittr)

scifi_folder = file.path('.', pattern='scifi')
fiction_literature_folder = file.path('.', 'fiction_literature')
humor_folder = file.path('.', 'humor')
thriller_folder = file.path('.', 'thriller')

scifi_docs = Corpus(DirSource(scifi_folder), readerControl=list(reader=readPlain))
fiction_literature_docs = Corpus(DirSource(fiction_literature_folder), readerControl=list(reader=readPlain))
humor_docs = Corpus(DirSource(humor_folder), readerControl=list(reader=readPlain))
thriller_docs = Corpus(DirSource(thriller_folder), readerControl=list(reader=readPlain))

