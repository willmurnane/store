from django.http import HttpResponse
from django.shortcuts import render_to_response
from store.models import FandomHierarchy, Image
from store.itemfilters import ApplyPredicates

def frontpage(request):
	# add_related_count(FandomHierarchy.objects.all(), Image, 'foo', 'sub_images', cumulative=True)
	tree = FandomHierarchy.objects.extra(select={"sub_images": """
		SELECT (
			SELECT COUNT(DISTINCT image_id) from %(join_table)s WHERE fandomhierarchy_id in (
				SELECT id FROM %(data_table)s m2 where m2.tree_id = %(data_table)s.tree_id
				                                   and m2.lft between %(data_table)s.lft and %(data_table)s.rght
			)
		)
		""" % {"data_table": "store_fandomhierarchy", "join_table": "store_image_fandoms"}
		})
	
	print tree.query.get_compiler('default').as_sql()[0]
	return render_to_response('index.html', {'filter': None, 'tree': tree})

def filtered(request, predicate):
	items = Image.objects.all()
	items = ApplyPredicates(predicate, items)
	print items
	print items.query.get_compiler('default').as_sql()
	print items.all()
	return render_to_response('by_category.html', {'items': items})
