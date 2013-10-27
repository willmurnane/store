import django.forms
import django.utils.safestring
from store.models import Pattern, Media

class SearchForm(django.forms.Form):
	query = django.forms.CharField(label="Search")

class ItemForm(django.forms.Form):
	def __init__(self, *args, **kwargs):
		pattern_id = kwargs.pop('pattern_id', None)
		super(ItemForm, self).__init__(initial = {'pattern_id': pattern_id}, *args, **kwargs)
	pattern_id = django.forms.ModelChoiceField(queryset=Pattern.objects, widget=django.forms.HiddenInput)
	media_option = django.forms.ModelChoiceField(queryset=Media.objects, widget=django.forms.RadioSelect, empty_label=None)
	media_orientation = django.forms.ChoiceField(choices=(('portrait', 'Portrait'), ('landscape', 'Landscape')), widget=django.forms.RadioSelect)
