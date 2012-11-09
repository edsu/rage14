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
    # ignore the mailing list address
    e = email.split("@")[0]
    return e in mboxes.lists

nodes = set()
edges = []
values = {}
sizes = {}

for email, from_email in g.subject_objects(nmo["from"]):
    from_email = scrub(from_email)
    nodes.add(from_email)
    sizes[from_email] = sizes.get(from_email, 0) + 1

    for to_email in g.objects(email, nmo.to):
        to_email = scrub(to_email)
        if is_list(to_email): continue
        sizes[to_email] = sizes.get(to_email, 0) + 1
        nodes.add(to_email)
        edges.append((from_email, to_email))

    for cc_email in g.objects(email, nmo.to):
        cc_email = scrub(cc_email)
        if is_list(cc_email): continue
        sizes[cc_email] = sizes.get(cc_email, 0) + 1
        nodes.add(cc_email)
        edges.append((from_email, cc_email))

# rewrite edges using node index
nodes = list(nodes)
nodes.sort()

links = []
values = {}
for a, b in edges:
    links.append({
        "source": nodes.index(a),
        "target": nodes.index(b),
    })

nodes = [{"name": v, "size": sizes[v]} for v in nodes]

# write the data out as javascript suitable for loading
d3 = {"nodes": nodes, "links": links} 
fh = open("d3.json", "w").write(json.dumps(d3, indent=2))
