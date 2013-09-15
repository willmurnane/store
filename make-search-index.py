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

schema = Schema(title=TEXT(stored=True), 
	tags=TEXT(stored=True),
	content=TEXT(stored=True),
	path=ID(stored=True),
)
if not os.path.exists(index_path):
  os.mkdir(index_path)
ix = create_in(index_path, schema)

writer = ix.writer()

def addDoc(title, path, tags, content):
	writer.add_document(title=title, path=path, tags=tags, content=content)

for item in store.models.Image.objects.all():
	fandom_string = ", ".join(map(lambda f: f.fullName, item.fandoms.all()))
	print item.name, fandom_string
	addDoc(
		title=item.name,
		path=unicode("/items/%d" % item.id),
		tags=unicode(fandom_string),
		content=u"",
	)

for item in store.models.FandomHierarchy.objects.all():
	addDoc(
		title=item.fullName,
		path=unicode("/filter/fandom=%d-%d" % (item.lft, item.rght)),
		tags=u"",
		content=u"",
	)

writer.commit()
