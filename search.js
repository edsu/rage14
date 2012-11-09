/**
 * use google to look for sites that mention httpRange-14
 */

var google = require("google");

/*
google("httpRange-14", function(err, next, hits) {
  for (var i = 0; i < hits.length; i++) {
    var hit = hits[i];
    console.log(hit.link);
  }
  if (next) next();
});
*/

google('site:ietf.org "httpRange-14"', function(err, next, hits) {
  for (var i = 0; i < hits.length; i++) {
    var hit = hits[i];
    console.log(hit.link);
  }
  if (next) next();
});
