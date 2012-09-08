from django.http import HttpResponse

def frontpage(request):
	return HttpResponse("Hello Store!")
