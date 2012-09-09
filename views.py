from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy, Image
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

def filtered(request, predicate):
	items = Image.objects.all()
	items = ApplyPredicates(predicate, items).all()
	query1 = copy.deepcopy(connection.queries)
	rval = render_to_response('by_category.html', {'items': items, "debug": debug_extras()})
	query2 = copy.deepcopy(connection.queries)
	
	print "Query1:", query1
	print "Query2:", query2
	return rval