from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy
from store.itemfilters import ApplyPredicates

def frontpage(request, filter=None):
	nodes = FandomHierarchy.objects.all()
	if filter:
		nodes = ApplyPredicates(filter, nodes)
		
	return render_to_response('index.html', {'filter': filter, 'nodes': nodes})
