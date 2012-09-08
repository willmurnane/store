from store.models import FandomHierarchy, Image, Media
from mptt.admin import MPTTModelAdmin
from django.contrib import admin

admin.site.register(FandomHierarchy, MPTTModelAdmin)
admin.site.register(Image)
admin.site.register(Media)
