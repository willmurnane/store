import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from store.models import FandomHierarchy, Image, Media, Pattern, Item, ImageItem
from store.itemfilters import ApplyPredicates
from django.conf import settings
import copy
from django.db import connection
from store.search import doSearch
from decorators import render_to
from forms import SearchForm, ItemForm
from cart import Cart
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@render_to('index.html')
def frontpage(request):
	# add_related_count(FandomHierarchy.objects.all(), Image, 'foo', 'sub_images', cumulative=True)
	return {'breadcrumbs': [[{'url': '/', 'text': 'Home'}]]}

def payment(request, result):
	if result == "success":
		return render_to_response('thanks.html', {'breadcrumbs': [[{'url': '/', 'text': 'Home'}, {'url': '/thanks', 'text': 'Thank you for your payment!'}]]})
	return frontpage(request)

@render_to('by_category.html')
def filtered(request, predicate):
	patterns, path = ApplyPredicates(predicate, Pattern.objects.all().select_related('image__name'))
	bc = [[{'url': '/', 'text': 'Home'}]]
	for crumb in path:
		bc[0].append({'url': '/filter/fandom=%d-%d' % (crumb.lft, crumb.rght), 'text': crumb.name})
	children = path.reverse()[0].get_children()
	for crumb in children:
		bc.append([{'url': '/filter/fandom=%d-%d' % (crumb.lft, crumb.rght), 'text': crumb.name}])
	page = request.GET.get('page')
	p = Paginator(patterns, 40)
	try:
		patterns = p.page(page)
	except PageNotAnInteger:
		patterns = p.page(1)
	except EmptyPage:
		patterns = p.page(p.num_pages)
	return {'patterns': patterns, 'breadcrumbs': bc}


def findImageScaling(w, h):
	goalWidth, goalHeight = 400, 400
	imageScale = max(min(int(goalWidth / w), int(goalHeight / h)), 1)
	return { "width": w * imageScale, "height": h * imageScale }

@render_to('pattern.html')
def pattern_page(request, pattern_id):
	pattern = get_object_or_404(Pattern, pk=pattern_id)
	return {
		'pattern': pattern,
		'scale': findImageScaling(pattern.pixel_width, pattern.pixel_height),
		'media': Media.objects.all(),
		'breadcrumbs': [[{'url': '/', 'text': 'Home'}]],
		'carthelper': ItemForm(pattern_id=pattern_id),
	}

@render_to('search_results.html')
def search_results(request):
	if request.method == 'GET':
		form = SearchForm(request.GET)
		if form.is_valid():
			results = doSearch(form.cleaned_data['query'])
			return {
				'query': form.cleaned_data['query'],
				'results': results,
			}
	return {}

def add_to_cart(request):
	form = ItemForm(request.POST or None)
	if form.is_valid():
		cart = Cart(request)
		row = ImageItem(
			pattern=form.cleaned_data['pattern_id'],
			media=form.cleaned_data['media_option'],
			media_orientation=form.cleaned_data['media_orientation'],
			extra_text='',
			special_instructions=''
			)
		row.save()
		cart.add(row, form.cleaned_data['media_option'].price_cents / 100, 1)
	else:
		logging.debug("Invalid form!")
		logging.debug(request)
		logging.debug(dir(request))
		# fixme: redirect to wherever we came from?
	return HttpResponseRedirect(reverse('show_cart'))

def remove_from_cart(request, item_id):
	cart = Cart(request)
	item = Item.objects.get(pk=item_id, cart=cart.cart)
	if item: item.delete()
	return HttpResponseRedirect(reverse('show_cart'))

@render_to('cart.html')
def show_cart(request):
	return { 'cart': Cart(request) }
