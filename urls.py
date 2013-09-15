from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^store/', include('store.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^items/(?P<item_id>\d+)', 'store.views.item_page'),
    (r'^filter/(?P<predicate>.+)', 'store.views.filtered'),
    (r'^payment/(?P<result>.+)', 'store.views.payment'),
    (r'^search', 'store.views.search_results'),
    (r'', 'store.views.frontpage'),
)
