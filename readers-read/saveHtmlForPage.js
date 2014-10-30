var request = require('request');
var fs = require('fs');
var Q = require('q');

var saveHtmlForPage = function(url, saveLocation) {
  var deferred = Q.defer();
  request(url, function(err, response, body) {
    if (err) {
      Q.reject(err);
    } else {
      fs.writeFile(saveLocation, body, function(err) {
        if (err) {
          Q.reject(err);
        } else {
          Q.resolve(response.text);
        }
      });
    }
  });
  return deferred.promise;
};

// saveHtmlForPage('http://www.readersread.com/excerpts/', 'html/home_page.html');

module.exports = saveHtmlForPage;