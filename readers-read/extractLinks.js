var Q = require('q');
var fs = require('fs');
var saveHtmlForPage = require('./saveHtmlForPage');

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
  var GetBookFunction = function(book) {
    return function() {
      console.log(book.title);
    }
  };
  books = books.map(function(book, index) {
    saveHtmlForPage(book.link, 'html/books/' + index + '_' + book.category + '.html');
  });
  
  return Q.all(books);
})


.done(function() {},function(err) { throw err; });
