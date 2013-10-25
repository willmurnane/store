import django.forms
import django.utils.safestring
from store.models import Image, RotatedMedia

class SearchForm(django.forms.Form):
	query = django.forms.CharField(label="Search")

class ItemForm(django.forms.Form):
	def __init__(self, *args, **kwargs):
		item_id = kwargs.pop('item_id', None)
		super(ItemForm, self).__init__(initial = {'item_id': item_id}, *args, **kwargs)
	item_id = django.forms.ModelChoiceField(queryset=Image.objects, widget=django.forms.HiddenInput)
	media_option = django.forms.ModelChoiceField(queryset=RotatedMedia.objects, widget=django.forms.RadioSelect)
