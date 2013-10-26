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
    (r'^admin', include(admin.site.urls)),
    url(r'^items/(?P<item_id>\d+)', 'store.views.item_page', name='item_page'),
    (r'^filter/(?P<predicate>.+)', 'store.views.filtered'),
    (r'^payment/(?P<result>.+)', 'store.views.payment'),
    url(r'^search', 'store.views.search_results', name='search'),
    url(r'^cart/add', 'store.views.add_to_cart', name='add_to_cart'),
    url(r'^cart/show', 'store.views.show_cart', name='show_cart'),
    url(r'^cart/remove/(?P<item_id>\d+)', 'store.views.remove_from_cart', name='remove_from_cart'),
    (r'', 'store.views.frontpage'),
)
