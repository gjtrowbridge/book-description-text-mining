
var textMining = {};

textMining.updateZScores = function(book, totalWordCounts) {
  book.zScores = [];

  var universalOverallCount = totalWordCounts.__totalCount;
  var bookOverallCount = book.wordCounts.__totalCount;

  var scaleBy = 10000;
  universalOverallCount /= scaleBy;
  bookOverallCount /= scaleBy;

  for (word in book.wordCounts) {
    var universalWordCount = totalWordCounts[word];
    var universalRate = universalWordCount / universalOverallCount;

    var bookWordCount = book.wordCounts[word];
    var bookWordRate = bookWordCount / bookOverallCount;

    var zScore = (bookWordRate - universalRate) / Math.sqrt(universalRate);
    book.zScores.push([word, zScore]);
  }
  book.zScores = book.zScores.sort(function(a, b) {
    return b[1] - a[1];
  });
  return book;
};


textMining.updateWordCounts = function(book, totalWordCounts) {
  book.wordCounts = {
    __totalCount: 0
  };

  var words = book.excerpt.split(/\s+/);
  for (var i=0; i<words.length; i++) {
    var word = words[i];
    if (book.wordCounts.hasOwnProperty(word)) {
      book.wordCounts[word]++;
    } else {
      book.wordCounts[word] = 1;
    }
    if (totalWordCounts.hasOwnProperty(word)) {
      totalWordCounts[word]++;
    } else {
      totalWordCounts[word] = 1;
    }
    book.wordCounts.__totalCount++;
    totalWordCounts.__totalCount++;
  }

  return book;
};

module.exports = textMining;