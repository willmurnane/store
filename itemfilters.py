import re

filter_router = {}

def RegisterFilter(regex, func):
	filter_router[regex] = func

def FindFilter(filtertext):
	for regex in filter_router:
		matches = regex.match(filtertext)
		if matches:
			return filter_router[regex](*matches.groupdict())
	throw

def byFandom(**kwargs):
	return lambda(nodes): nodes.filter(fandom_id=fandomId)

def __init__():
	RegisterFilter("^fandom=(?P<fandomId>\d+)", byFandom)

"""Select a subset of items based on the filter described by filters"""
def ApplyPredicates(filters, items):
	filter_list = filters.split(',')
	for filter in filter_list:
		items = FindFilter(filter)(items)