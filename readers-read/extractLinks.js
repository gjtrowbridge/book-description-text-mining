var Q = require('q');
var fs = require('fs');
var saveHtmlForPage = require('./saveHtmlForPage');
var preprocessText = require('./preprocessText');
Q.longStackSupport = true;

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

// .then(function(books) {
//   books = books.map(function(book, index) {
//     saveHtmlForPage(book.link, 'html/books/' + index + '_' + book.category + '.html');
//   });
  
//   return Q.all(books);
// })

.then(function(books) {
  books = books.map(function(book, index) {
    book.index = index;
    book.htmlPath = 'html/books/' + index + '_' + book.category + '.html';
    book.textPath = 'preprocessed/' + index + '_' + book.category + '_' + book.shortTitle + '.txt';
    return preprocessText(book);
  });
  return Q.all(books);
})

.done(function() {},function(err) { throw err; });
