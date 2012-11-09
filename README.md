Notes and code for my "A humanist's look at Linked Data" paper/talk.

email discussion
----------------

I wanted to visualize the discussion around httpRange-14, so I wrote
some scripts to pull down email discussions.

* search.js - searches google for URLs that mention httpRange-14
* mboxes.py - download w3 mailing list archives for discussion lists identified
  by search.js
* load.py - read the mbox files looking for emails that mention httpRange-14 and
  save the social graph as RDF.
* d3.py - write out the rdf data as json suitable for use by d3
