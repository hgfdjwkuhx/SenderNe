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

class TempThread_Command:
    temp_thread = None

    @staticmethod
    def run_sockets():
        import threading
        TempThread_Command.temp_thread = threading.Thread(target=TempThread_Command._run_sockets)
        TempThread_Command.temp_thread.start()

    @staticmethod
    def _run_sockets():
        from SenderNeClientWS.management.commands import run_senderNeWS_server
        bb = run_senderNeWS_server.Command()

    @staticmethod
    def _run_socket01():
        from SenderNeClientWS.TestSockets.testSocket01 import start_server

@api_view(['GET'])
def testConnection(request):
    Title = 'ClientAPI_testConnection'

    #TempThread_Command.run_sockets()
    TempThread_Command._run_socket01()

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


class ListTodo(generics.ListCreateAPIView):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer




