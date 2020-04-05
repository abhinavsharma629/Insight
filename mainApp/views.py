#IMPORTS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Document
from .utils import add_data_or_400, delete_data_or_404
from .serializers import DocumentSerializer


class Actions(APIView):

    #GET Data
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        if('data_id' in request.GET):
            data_id=request.GET.get('data_id')
            if(Document.objects.filter(owner=request.user, pk=data_id).count()>0):
                obj=Document.objects.get(owner=request.user, pk=data_id)
                serializer=DocumentSerializer(obj)
                return Response({"data":serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message':"Error"}, status=status.HTTP_404_NOT_FOUND)
        elif('all' in request.GET):
            obj=Document.objects.filter(owner=request.user)
            serializer=DocumentSerializer(obj, many=True)
            return Response({"data-list":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"Provide The Data Id"}, status=status.HTTP_400_BAD_REQUEST)


    permission_classes=(IsAuthenticated,)
    # SAVE Data
    def post(self, request, format=None):
        parser_classes = (JSONParser,)
        obj,status1=add_data_or_400(request)
        if(status1==201):
            serializer= DocumentSerializer(obj)
            return Response({'message':"Successfully Saved Data", "details":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':"Error"}, status=status.HTTP_400_BAD_REQUEST)


    permission_classes=(IsAuthenticated,)
    # Delete data
    def delete(self, request, format=None):
        parser_classes = (JSONParser,)
        status1=delete_data_or_404(request)
        if(status1==200):
            return Response({'message':"Successfully Deleted Data"}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"Error"}, status=status.HTTP_404_NOT_FOUND)
