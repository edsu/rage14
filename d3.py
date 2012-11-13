#!/usr/bin/env python

# read rdf and write out some json for sigma.js to use

import json
import rdflib
import mboxes

nmo = rdflib.Namespace("http://www.semanticdesktop.org/ontologies/nmo/#")
g = rdflib.Graph("Sleepycat", identifier="emails")
g.open("store")

def scrub(email):
    return email.replace("mailto:", "").lower()

def is_list(email):
    e = email.split("@")[0]
    return e in mboxes.lists

# create graph of people who have corresponded with each other

people = set()
correspondence = []
senders = {} 

for email, from_email in g.subject_objects(nmo["from"]):
    from_email = scrub(from_email)
    people.add(from_email)
    senders[from_email] = senders.get(from_email, 0) + 1

    for to_email in g.objects(email, nmo.to):
        to_email = scrub(to_email)
        if is_list(to_email): continue
        people.add(to_email)
        correspondence.append((from_email, to_email))

    for cc_email in g.objects(email, nmo.to):
        cc_email = scrub(cc_email)
        if is_list(cc_email): continue
        people.add(cc_email)
        correspondence.append((from_email, cc_email))

people = list(people)
people.sort()
people = [{"name": v, "sent": senders.get(v, 0)} for v in people]
people = filter(lambda p: p["sent"] != 0, people)
people_ids = [p["name"] for p in people]

links = []
for a, b in correspondence:
    if a in people_ids and b in people_ids:
        links.append({
            "source": people_ids.index(a),
            "target": people_ids.index(b),
        })

d3 = {"nodes": people, "links": links} 
fh = open("people.json", "w").write(json.dumps(d3, indent=2))


# create a graph of email discussions, where nodes are 
# email messages and edges are replies

emails = set()
replies = []
for reply, orig in g.subject_objects(nmo.inReplyTo):
    emails.add(reply)
    emails.add(orig)
    replies.append((reply, orig))

emails = list(emails)
emails.sort()
email_nodes = []
for email in emails:
    f = g.value(email, nmo["from"], None)
    s = g.value(email, nmo.messageSubject, None)
    r = g.value(email, nmo.inReplyTo, None)
    if f and s:
        f = f.replace("mailto:", "")
        email_nodes.append({
            "subject": s, 
            "from": f,
            "url": email,
            "replyTo": r
        })

emails = [e["url"] for e in email_nodes]
links = []
for a, b in replies:
    if a in emails and b in emails:
        links.append({
            "source": emails.index(a),
            "target": emails.index(b)
        })

d3 = {"nodes": email_nodes, "links": links}
fh = open("emails.json", "w").write(json.dumps(d3, indent=2))
