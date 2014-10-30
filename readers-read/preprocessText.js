var fs = require('fs');
var Q = require('q');


var saveTextToPage = function(text, saveLocation) {
  return Q.ninvoke(fs, 'writeFile', saveLocation, text);
};

var isStartOfExcerpt = function(line) {
  var re = /^<\/table>$/;
  if (re.exec(line)) {
    return true;
  } else {
    return false;
  }
};
var isEndOfExcerpt = function(line) {
  var re = /excerpted from/;
  if (re.exec(line)) {
    return true;
  } else {
    return false;
  }
};

var count = 0;
var preprocessText = function(book) {
  // Read in book data
  return Q.ninvoke(fs, 'readFile', book.htmlPath, 'utf8')
  .then(function(data) {
    var lines = data.split('\n');
    var startIndex = 0;
    var endIndex = 0;

    for (var i=0; i<lines.length; i++) {
      lines[i] = lines[i].toLowerCase();
      var line = lines[i];
      if (isStartOfExcerpt(line)) {
        startIndex = i;
      } else if (isEndOfExcerpt(line)) {
        endIndex = i;
        break;
      }
    }
    book.excerpt = lines.slice(startIndex + 1, endIndex).join(' ');
    book.excerpt = book.excerpt.replace(/<[^>]*>/g, ' ');
    book.excerpt = book.excerpt.replace(/[^\w\s]*/g, '');
    book.excerpt = book.excerpt.replace(/\s{2,}/g, ' ');
    // book.excerpt = book.excerpt.replace(/<([a-z]|"|=|,|#|-)*>/g, ' ');
    // book.excerpt = book.excerpt.replace(/<\/([a-z]|"|)*>/g, ' ');
    // book.excerpt = book.excerpt.replace(/<[^a-z\s']>/g, '');
    // book.excerpt = book.excerpt.replace(/<\w*>/, '');
    // book.excerpt = book.excerpt.replace('</p>', '');
    // book.excerpt = book.excerpt.replace('<b>', '');

    return saveTextToPage(book.excerpt, book.textPath);
  })

  .then(function() {

  })
  // Cut out everything except the book description

  
};

module.exports = preprocessText;
