from django.conf.urls import include, url
from SenderNeClientAPI.views import ClientAPI , FreeClientAPI

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

    #----------------- new client ----------------------------#
    url(r'^be_new/$',FreeClientAPI.temp_new_client , name = 'Home.AA'),
    url(r'^socketInfo/(?P<user_identifier>[\w\-]+)/$',FreeClientAPI.get_token_tempClient , name = 'Home.BB'),


]


