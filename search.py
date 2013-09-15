import os
import sys
import store.models
import store.settings
from whoosh.index import *
from whoosh.query import *
from whoosh.qparser import QueryParser

class SearchResult:
	def __init__(self, name, tags, highlights, path):
		self.name = name
		self.tags = tags
		self.highlights = highlights
		self.path = path

def doSearch(query):
	ix = open_dir(store.settings.index_path)
	with ix.searcher() as s:
		my_query = Or([Variations("content", unicode(query)), Variations("title", unicode(query)), Variations("tags", unicode(query))])
		results = s.search(my_query, terms=True)
		rval = []
		for item in results:
			rval.append(SearchResult(
				item.fields()['title'],
				item.fields()['content'],
				dict([(foo[0], item.highlights(foo[0])) for foo in item.matched_terms()]),
				item.fields()['path']
			))
		return rval
