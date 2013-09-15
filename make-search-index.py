#! /usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import sys
sys.path.append("..")
import store.models
from whoosh.index import *
from whoosh.fields import *

index_path = "index"

schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), path=ID(stored=True))
if not os.path.exists(index_path):
  os.mkdir(index_path)
ix = create_in(index_path, schema)

writer = ix.writer()

def addDoc(title, path, content):
	writer.add_document(title=title, path=path, content=content)

for item in store.models.Image.objects.all():
	fandom_string = ", ".join(map(lambda f: f.name, item.fandoms.all()))
	addDoc(
		title=item.name,
		path=unicode("/items/%d" % item.id),
		content=unicode(fandom_string),
	)

for item in store.models.FandomHierarchy.objects.all():
	print item
	ancs = [x.name for x in item.get_ancestors()]
	ancs.append(item.name)
	title = u" \u00BB ".join(ancs)
	print title
	addDoc(
		title=title,
		path=unicode("/filter/fandom=%d-%d" % (item.lft, item.rght)),
		content=item.name,
	)

writer.commit()
