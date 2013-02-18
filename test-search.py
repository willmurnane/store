#! /usr/bin/python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import sys
sys.path.append("..")
import store.models
from whoosh.index import *
from whoosh.query import *
from whoosh.qparser import QueryParser

index_path = "index"

ix = open_dir(index_path)
print sys.argv[1:]

with ix.searcher() as s:
	for fields in s.all_stored_fields():
		print fields
#	terms = map(lambda w: Or([Term("content", unicode(w)), Term("title", unicode(w))]), sys.argv[1:])
	my_query = Term("content", unicode(sys.argv[1]))
#	qp = QueryParser("title", schema = ix.schema)
#	search = unicode(" ".join(sys.argv[1:]))
#	print search
#	my_query = qp.parse(search)
	print my_query
	results = s.search(my_query)
	print results
	print "%d results found\n" % len(results)
	for item in results:
		print item
