from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy, Image
from store.itemfilters import ApplyPredicates

def frontpage(request):
	tree = FandomHierarchy.objects.all()
	return render_to_response('index.html', {'filter': None, 'tree': tree})

def filtered(request, filter):
	tree = FandomHierarchy.objects.all()
	items = Image.objects.all()
	if filter:
		items = ApplyPredicates(filter, items)
	return render_to_response('index.html', {'filter': filter, 'tree': tree, 'items': items})
