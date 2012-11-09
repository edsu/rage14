#!/usr/bin/env python

import os
import re
import rdflib
import rfc822
import mailbox 
import datetime

nmo = rdflib.Namespace("http://www.semanticdesktop.org/ontologies/nmo/#")
rdf = rdflib.RDF
uri = rdflib.URIRef

def main():
    generate_rdf()

def generate_rdf():
    g = rdflib.Graph("Sleepycat", identifier="emails")
    g.open("store", create=True)
    g.bind("nmo", str(nmo))
    for msg in range14_messages():
        u = uri(msg["url"])
        print u
        g.add((u, rdf.type, nmo.Email))
        g.add((u, nmo["from"], uri("mailto:" + msg["from"][1])))
        g.add((u, nmo.sentDate, rdflib.Literal(msg["date"])))
        g.add((u, nmo.messageSubject, rdflib.Literal(msg["subject"])))
        for name, email in msg["to"]:
            g.add((u, nmo.to, uri("mailto:" + email)))
        for name, email in msg["cc"]:
            g.add((u, nmo.cc, uri("mailto:" + email)))
    g.serialize(open("emails.rdf", "w"))
    g.serialize(open("emails.ttl", "w"), format="turtle")
    g.close()

def get_message(msg):
    fr = rfc822.parseaddr(msg['from'])
    to = rfc822.AddressList(msg['to']).addresslist
    cc = rfc822.AddressList(msg['cc']).addresslist
    subject = msg['subject']
    date = rfc822.parsedate(msg['date'])
    date = datetime.datetime(*date[:6])
    url = msg['Archived-At']
    if not url: 
        url = msg['X-Archived-At']
    url = url.strip("<>")

    return {
        "from": fr,
        "subject": subject,
        "to": to,
        "cc": cc,
        "url": url,
        "date": date,
        "raw": msg.as_string()
    }

    return None

def range14_messages():
    for root, dirs, files in os.walk("mboxes"):
        for filename in files:
            mbox_file = os.path.join(root, filename)
            count = 0
            for msg in mailbox.mbox(mbox_file):
                count += 1
                try:
                    m = get_message(msg)
                    if re.search("httpRange-?14", m["raw"], re.IGNORECASE):
                        yield m
                except Exception, e: 
                    print "unable to add message #%s from %s: %s" % (count, mbox_file, e)

if __name__ == "__main__":
    main()
