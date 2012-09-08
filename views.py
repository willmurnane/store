from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy, Image
from store.itemfilters import ApplyPredicates

def frontpage(request):
	tree = FandomHierarchy.objects.all()
	return render_to_response('index.html', {'filter': None, 'tree': tree})

def filtered(request, filter):
	tree = Image.objects.all()
	if filter:
		tree = ApplyPredicates(filter, tree)
	return render_to_response('index.html', {'filter': filter, 'tree': tree})
