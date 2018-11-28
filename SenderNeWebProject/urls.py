"""
Definition of urls for SenderNeWebProject.
"""

from datetime import datetime
import site
from django.conf.urls import url , include
import django.contrib.auth.views

import app.forms
import app.views
import SenderNeClientAPI

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()



#############################################################################
import django.contrib.auth.views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()


urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),







    ##########################################################################
        url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/' , include('django.contrib.admindocs.urls')),
    #url(r'^admin/', include('django.contrib.admin.site.urls')),
    #url(r'' , admin.site.urls),
    #url(r'', include(admin.site.urls)),



    ############################# : Apps : ####################################

    ###### Whats Manger  #####
    url(r'', include('SenderNeClientAPI.urls'))     ,


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

