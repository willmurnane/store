import re
from store.models import FandomHierarchy

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
	return lambda nodes: ((nodes.filter(fandoms__lft__gte=fandomIdMin, fandoms__rght__lte=fandomIdMax).distinct()),
		FandomHierarchy.objects.get(lft=fandomIdMin).get_ancestors(include_self=True))

"""Select a subset of items based on the filter described by filters"""
def ApplyPredicates(filters, items):
	filter_list = filters.split(',')
	for filter in filter_list:
		foo = FindFilter(filter)
		items, path = foo(items)
	return items, path


RegisterFilter("^fandom=(?P<fandomIdMin>\d+)-(?P<fandomIdMax>\d+)", byFandom)
