import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.template import RequestContext
from django import forms
import json

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
def testConnection(request):
    Title = 'ClientAPI_testConnection'


    resultt = {
        "connect" : True,
        "services_able" : True,
    }



    return JsonResponse(resultt , safe = True)

#************************* Trying ***********************#

# api/views.py
from rest_framework import generics

from SenderNeClientAPI import  models
from SenderNeClientAPI import serializers



