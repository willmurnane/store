from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.inclusion_tag('add_button.html')
def add_button(item):
	return {'item': item}

@register.inclusion_tag('small_block.html')
def small_block(item):
	return {'item': item}
