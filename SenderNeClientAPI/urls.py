from django.conf.urls import include, url
from SenderNeClientAPI.views import ClientAPI

#from django.urls import path
app_name = 'SenderNeClientAPI'


urlpatterns =[

    ##### Home ####
    url(r'^client/$',ClientAPI.testConnection , name = 'Home'),

    #----------------------------------------------------#
    url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^rest-auth/registration/', include('rest_auth.registration.urls', namespace="rest_auth.registration")),
    #----------------------------------------------------#

    #url(r'^ContactsManager/test/RemoveAll/$',home.test_RemoveAll , name = 'test.removeAll'),
    #url(r'^ContactsManager/test/remove/whatsContacts/$',home.Test_RemoveWhatsContacts , name = 'test.remove.whatsContacts'),


]


