var Q = require('q');
var fs = require('fs');
var saveHtmlForPage = require('./saveHtmlForPage');
var preprocessText = require('./preprocessText');
var textMining = require('./textMining');
var stopWords = require('stopwords').english;

Q.longStackSupport = true;

var stopWordsDict = {
  '': true,
  'chapter': true
};
for (var i=0; i<stopWords.length; i++) {
  var word = stopWords[i];
  stopWordsDict[word] = true;
}

var extractLinks = function(filePath) {
  return Q.ninvoke(fs, 'readFile', filePath, 'utf8')

  .then(function(data) {
    var lines = data.split('\n');
    var books = [];
    var book = {
      category: 'children'
    };
    var category;

    for (var i=0; i<lines.length; i++) {
      // Save the current book
      // then create a new book
      if (book.title) {
        books.push(book);
        book = {};
        book.category = category;
      }
      var line = lines[i].toLowerCase();

      var title = isTitle(line);
      var link = isLink(line);
      category = isCategory(line) || category;

      // Update book info as we find it
      if (title) {
        book.title = title;
      }

      if (link) {
        book.link = link;
      }

      if (book.link && book.title) {
        var re = /\/([^\/]*).html?$/;
        var shortTitle = re.exec(book.link)[1];
        book.shortTitle = shortTitle;
      }
    }
    return books;
  })

};

// Check if given line is a book category
var isCategory = function(line) {
  var re = /^<a name="(.*)"/;
  var arr = re.exec(line);
  if (arr) {
    return arr[1];
  } else {
    return false;
  }
};

// Check if given line is a book link
var isLink = function(line) {
  var re = /<a href="(.*)">/;
  var arr = re.exec(line);
  if (arr) {
    return arr[1];
  } else {
    return false;
  }
};

// Check if given line is a book title
var isTitle = function(line) {
  var re = /<i><b>(.*)<\/b><\/i>/;
  var arr = re.exec(line);
  if (arr) {
    return arr[1];
  } else {
    return false;
  }
};

extractLinks('html/home_page.html')

.then(function(books) {
  books = books.map(function(book, index) {
    book.index = index;
    book.htmlPath = 'html/books/' + index + '_' + book.category + '.html';
    book.textPath = 'preprocessed/' + index + '_' + book.category + '_' + book.shortTitle + '.txt';
    return book;
  });
  return books;
})

// .then(function(books) {
//   books = books.map(function(book, index) {
//     return saveHtmlForPage(book.link, 'html/books/' + index + '_' + book.category + '.html');
//   });
  
//   return Q.all(books);
// })

.then(function(books) {
  books = books.map(function(book, index) {
    return preprocessText(book);
  });
  return Q.all(books)
})

// Calculate z-scores
.then(function(books) {
  var totalWordCounts = {
    __totalCount: 0
  };
  for (var i=0; i<books.length; i++) {
    textMining.updateWordCounts(books[i], totalWordCounts, stopWordsDict);
  }
  for (var i=0; i<books.length; i++) {
    textMining.updateZScores(books[i], totalWordCounts);
  }
  return books;
})

// Count common keywords across groups
.then(function(books) {
  var zScoreCutoff = 5;
  var topHits = {};
  var category = 'children';
  for (var i=0; i<books.length; i++) {
    var book = books[i];
    if (book.category === category) {
      for (var j=0; j<book.zScores.length; j++) {
        var keyword = book.zScores[j][0];
        var zScore = book.zScores[j][1];
        if (zScore >= zScoreCutoff) {
          if (topHits.hasOwnProperty(keyword)) {
            var th = topHits[keyword];
            th.total += zScore;
            th.count++;
            if (th.minZScore > zScore) {
              th.minZScore = zScore;
            }
            if (th.maxZScore < zScore) {
              th.maxZScore = zScore
            }
          } else {
            topHits[keyword] = {
              count: 1,
              total: zScore,
              minZScore: zScore,
              maxZScore: zScore
            }
          }
        }
      }
    }
  }
  var sortedTopHits = [];
  for (keyword in topHits) {
    var th = topHits[keyword];
    sortedTopHits.push([keyword, th.count, th.minZScore, th.total]);
  }
  sortedTopHits = sortedTopHits.sort(function(a,b) {
    return b[1] - a[1];
  });
  return {
    books: books,
    topHits: sortedTopHits,
    category: category,
    zScoreCutoff: zScoreCutoff
  };
})

.then(function(data) {
  var useTopX = 100;
  var books = data.books;
  var topHits = data.topHits.slice(0, useTopX);
  var outputIndicators = true;

  var headers = topHits.map(function(arr) {
    return '"' + arr[0] + '"';
  });

  var header = '"title" "category" ' + headers.join(' ');
  
  var lines = books.map(function(book, index) {
    var features = topHits.map(function(arr) {
      var keyword = arr[0];
      var zScore;
      var present = 0;
      if (book.zScoresDict.hasOwnProperty(keyword)) {
        zScore = book.zScoresDict[keyword];
        present = 1;
      } else {
        var ur = textMining.universalRates[keyword];
        zScore = -1 * ur / Math.sqrt(ur);
        present = 0;
      }
      if (outputIndicators) {
        return present;
      } else {
        return zScore;
      }
    });
    features.unshift('"' + index + '" "' + book.shortTitle + '" "' + book.category + '"');
    return features.join(' ');
  });

  var result = header + '\n' + lines.join('\n');

  var outputPath = './structured_data/' + data.category + '_top_' +
      useTopX + '_zscores_above_' + data.zScoreCutoff + '_indicators_' +
      outputIndicators + '.txt';

  console.log(outputPath);

  return Q.ninvoke(fs, 'writeFile', outputPath, result);


})

// .then(function(books) {
//   var categories = {};
//   for (var i=0; i<books.length; i++) {
//     var book = books[i]
//     var category = book.category;

//     if (categories.hasOwnProperty(category)) {
//       categories[category].push(book);
//     } else {
//       categories[category] = [book];
//     }
//   }
//   for (category in categories) {
//     console.log(category, categories[category].length)
//   }
// })

.done(function() {},function(err) { throw err; });
