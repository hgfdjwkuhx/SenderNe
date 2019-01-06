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

from SenderNeClientAPI.models import TempUserPrivateProcessorInfo


@api_view(['GET'])
def temp_new_client(request):
    #Title = 'temp_new_client'

    temp = TempUserPrivateProcessorInfo()
    temp.save()

    return JsonResponse(temp.resultt_new() , safe = True)


def get_token_tempClient(request , user_identifier):
    #Title = 'get_token_tempClient'
    #return JsonResponse({"Title" : Title , "user_identifier" : user_identifier}, safe=True)

    if user_identifier is None:
        return JsonResponse({"error" : user_identifier}, safe=True)

    temp = TempUserPrivateProcessorInfo.objects.filter(user_identifier=user_identifier).first()
    if temp is None:
        return JsonResponse({"error" : user_identifier}, safe=True)

    return JsonResponse(temp.get_tokenInfo() , safe = True)


