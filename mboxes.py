#!/usr/bin/env python

# download mboxes for w3 discussion lists that have had httpRange-14 discussion
# you need to pass in your w3 username and password for the download to work

import os
import re
import sys
import time
import requests

requests.session().config['keep_alive'] = False

lists = (
    "public-awwsw",
    "public-lod",
    "public-rdf-wg",
    "public-swbp-wg",
    "public-vocabs",
    "semantic-web",
    "www-tag",
    "public-swd-wg",
    "public-sparql-dev",
)

def download(auth):
    for mlist in lists:
        url = "https://lists.w3.org/Archives/Public/%s/mboxes/" % mlist
        html = requests.get(url, auth=auth)
        for href in re.findall("'(\d+-\d+.mbx)'", html.content):
            mbox_url = url + href
            mbox_filename = "mboxes/%s/%s" % (mlist, href)
            # don't download if we have it already
            if os.path.isfile(mbox_filename):
                continue
            print mbox_url
            try:
                mbox = requests.get(mbox_url, verify=False, auth=auth).content
            except:
                print "couldn't fetch %s" % mbox_url
                continue
            if not os.path.isdir("mboxes/%s" % mlist):
                os.makedirs("mboxes/%s" % mlist)
            open(mbox_filename, "w").write(mbox)

if __name__ == "__main__":
    auth = (sys.argv[1], sys.argv[2])
    download(auth)
