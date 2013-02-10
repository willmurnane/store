from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from store.models import FandomHierarchy, Image, RotatedMedia
from store.itemfilters import ApplyPredicates
from django.conf import settings
import copy
from django.db import connection

def debug_extras(): return ""
if False: # settings.DEBUG:
	def real_debug():
		return connection.queries
	debug_extras = real_debug

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
	return render_to_response('index.html', {'filter': None, 'tree': tree, "debug": debug_extras()})

def payment(request, result):
	if result == "success":
		return render_to_response('thanks.html')
	return frontpage(request)
def filtered(request, predicate):
	items = Image.objects.all()
	items = ApplyPredicates(predicate, items).all()
	rval = render_to_response('by_category.html', {'items': items, "debug": debug_extras()})
	return rval


def findImageScaling(w, h):
	goalWidth, goalHeight = 400, 400
	imageScale = max(min(int(goalWidth / w), int(goalHeight / h)), 1)
	return { "width": w * imageScale, "height": h * imageScale }

def item_page(request, item_id):
	item = get_object_or_404(Image, pk=item_id)
	return render_to_response('item.html', 
	{
		'item': item,
		'scale': findImageScaling(item.pixel_width, item.pixel_height),
		'media': RotatedMedia.objects.all(),
		'debug': debug_extras()
	})

