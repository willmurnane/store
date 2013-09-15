from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from store.models import FandomHierarchy, Image, RotatedMedia
from store.itemfilters import ApplyPredicates
from django.conf import settings
import copy
from django.db import connection
from store.search import doSearch
from decorators import render_to
from forms import SearchForm

@render_to('index.html')
def frontpage(request):
	# add_related_count(FandomHierarchy.objects.all(), Image, 'foo', 'sub_images', cumulative=True)
	tree = FandomHierarchy.objects.extra(select={"sub_images": """
			SELECT COUNT(DISTINCT %(join_table_fk1_name)s) from %(join_table)s WHERE %(join_table_fk2_name)s in (
				SELECT id FROM %(data_table)s m2 where m2.tree_id = %(data_table)s.tree_id
				                                   and m2.lft between %(data_table)s.lft and %(data_table)s.rght
			)
		""" % {"data_table": "store_fandomhierarchy",
		       "join_table": "store_image_fandoms",
		       "join_table_fk1_name": "image_id",
		       "join_table_fk2_name": "fandomhierarchy_id",
		       }
		})
	
#	print tree.query.get_compiler('default').as_sql()[0]
	return {'tree': tree, 'breadcrumbs': [[{'url': '/', 'text': 'Home'}]]}

def payment(request, result):
	if result == "success":
		return render_to_response('thanks.html', {'breadcrumbs': [[{'url': '/', 'text': 'Home'}, {'url': '/thanks', 'text': 'Thank you for your payment!'}]]})
	return frontpage(request)

@render_to('by_category.html')
def filtered(request, predicate):
	items, path = ApplyPredicates(predicate, Image.objects.all())
	bc = [[{'url': '/', 'text': 'Home'}]]
	for crumb in path:
		bc[0].append({'url': '/filter/fandom=%d-%d' % (crumb.lft, crumb.rght), 'text': crumb.name})
	children = path.reverse()[0].get_children()
	for crumb in children:
		bc.append([{'url': '/filter/fandom=%d-%d' % (crumb.lft, crumb.rght), 'text': crumb.name}])
	return {'items': items, 'breadcrumbs': bc}


def findImageScaling(w, h):
	goalWidth, goalHeight = 400, 400
	imageScale = max(min(int(goalWidth / w), int(goalHeight / h)), 1)
	return { "width": w * imageScale, "height": h * imageScale }

@render_to('item.html')
def item_page(request, item_id):
	item = get_object_or_404(Image, pk=item_id)
	return {
		'item': item,
		'scale': findImageScaling(item.pixel_width, item.pixel_height),
		'media': RotatedMedia.objects.all(),
		'breadcrumbs': [[{'url': '/', 'text': 'Home'}]],
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