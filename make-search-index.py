#! /usr/bin/python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import sys
sys.path.append("..")
import store.models
from whoosh.index import *
from whoosh.fields import *

index_path = "index"

schema = Schema(title=TEXT, content=TEXT(stored=True), path=ID(stored=True))
if not os.path.exists(index_path):
  os.mkdir(index_path)
ix = create_in(index_path, schema)

writer = ix.writer()
for item in store.models.Image.objects.all():
	print item.name
	fandom_string = item.name + ": " + ", ".join(map(lambda f: f.name, item.fandoms.all()))
	writer.add_document(title=item.name, path=unicode("/items/%d" % item.id), content=unicode(fandom_string))

for item in store.models.FandomHierarchy.objects.all():
	writer.add_document(title=item.name, path=unicode("/filter/fandom=%d-%d" % (item.lft, item.rght)), content=item.name)
writer.commit()
