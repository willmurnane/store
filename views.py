from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy, Image
from store.itemfilters import ApplyPredicates

def frontpage(request):
	tree = FandomHierarchy.objects.all()
	return render_to_response('index.html', {'filter': None, 'tree': tree})

def filtered(request, predicate):
	items = Image.objects.all()
	items = ApplyPredicates(predicate, items)
	print items
	print items.query.get_compiler('default').as_sql()
	print items.all()
	return render_to_response('by_category.html', {'items': items})
