from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy

def frontpage(request):
	return render_to_response('index.html', {'nodes': FandomHierarchy.objects.all()})
