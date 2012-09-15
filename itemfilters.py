import re

filter_router = {}

def RegisterFilter(regex, func):
	filter_router[re.compile(regex)] = func

def FindFilter(filtertext):
#	print "Looking for match for \"%s\"" % filtertext
	for regex in filter_router:
		matches = regex.match(filtertext)
		if matches:
			return filter_router[regex](**matches.groupdict())
	raise "Couldn't find filter matching \"%s\"" % filtertext

def byFandom(fandomIdMin, fandomIdMax):
	return lambda(nodes): nodes.filter(fandoms__lft__gte=fandomIdMin, fandoms__rght__lte=fandomIdMax).distinct()

"""Select a subset of items based on the filter described by filters"""
def ApplyPredicates(filters, items):
	filter_list = filters.split(',')
	for filter in filter_list:
		items = FindFilter(filter)(items)
	return items


RegisterFilter("^fandom=(?P<fandomIdMin>\d+)-(?P<fandomIdMax>\d+)", byFandom)
