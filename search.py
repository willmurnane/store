import os
import sys
import store.models
from whoosh.index import *
from whoosh.query import *
from whoosh.qparser import QueryParser

print os.getcwd()
index_path = "./index"

class SearchResult:
	def __init__(self, name, tags, highlights, path):
		self.name = name
		self.tags = tags
		self.highlights = highlights
		self.path = path

def doSearch(query):
	ix = open_dir(index_path)
	with ix.searcher() as s:
		my_query = Or([Variations("content", unicode(query)), Variations("title", unicode(query))])
		results = s.search(my_query, terms=True)
		rval = []
		print results.matched_terms()
		for item in results:
			print item.matched_terms()
			print "Hilite: '%s'" %  item.highlights("content")
			rval.append(SearchResult(
				item.fields()['title'],
				item.fields()['content'],
				dict([(foo[0], item.highlights(foo[0])) for foo in item.matched_terms()]),
				item.fields()['path']
			))
		return rval
