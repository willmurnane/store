from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def itemBlock(item, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda t: t
	result = """<div><a href="/items/%d"><img src="%s" /><br/>%s</a></div>""" % (item.id, item.image.url, esc(item.name))
	return mark_safe(result)

itemBlock.needs_autoescape = True

@register.filter
def mediadisplay(item, radioGroupName, autoescape=None):
	if autoescape:
		esc = conditional_escape
	else:
		esc = lambda t: t
	result = """<div><input type="radio" name="%s">%s%s</input></div>""" % \
	(
		esc(radioGroupName),
		esc(item.name),
		" " + item.orientation if item.rotateable else ""
	)
	return mark_safe(result)
mediadisplay.needs_autoescape = True

@register.filter
def mediarotated(item):
	
	item.visible_width, item.visible_height = item.visible_height, item.visible_width
	item.exterior_width, item.exterior_height = item.exterior_height, item.exterior_width
	item.isLandscape = True
	return item
