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
