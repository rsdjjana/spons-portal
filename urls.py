
from django.conf.urls.defaults import*
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', 'portal.views.log_in', name='login'),
    url(r'^$', 'portal.views.home', name='home'),
    url(r'^logout/$', 'portal.views.log_out', name='logout'),
	url(r'^register/$','portal.views.register',name='register'),
    # url(r'^portal/', include('portal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
