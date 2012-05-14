
from django.conf.urls.defaults import*
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'portal.views.log_in', name='login'),
	url(r'^register/$','portal.views.register',name='register'),
    url(r'^$', 'portal.views.home', name='home'),
	url(r'^addcategory/$','portal.views.add_category',name='addcategory'),
	url(r'^category/(\d+)/$','portal.views.view_events',name='viewevents'),
	url(r'^edit_category/(\d+)/$','portal.views.edit_category',name='edit_category'),
	url(r'^delete_category/(\d+)/$','portal.views.delete_category',name='delete_category'),
	url(r'^addevents/(\d+)/$','portal.views.add_events',name='addevents'),
	url(r'^edit_event/(\d+)/(\d+)/$','portal.views.edit_event',name='edit_event'),
	url(r'^delete_event/(\d+)/(\d+)/$','portal.views.delete_event',name='delete_event'),
    url(r'^logout/$', 'portal.views.log_out', name='logout'),
	
    # url(r'^portal/', include('portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
