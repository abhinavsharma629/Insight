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
from rest_framework import generics

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
        elif('all' in request.GET and request.GET.get('all').lower()=="true"):
            obj=Document.objects.filter(owner=request.user)
            serializer=DocumentSerializer(obj, many=True)
            return Response({"data-list":serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"Please provide the Data Id!!"}, status=status.HTTP_400_BAD_REQUEST)


    permission_classes=(IsAuthenticated,)
    # SAVE Data by manually extracting details/ meta-data of the file uploaded
    def post(self, request, format=None):
        parser_classes = (JSONParser,)
        obj,status1=add_data_or_400(request)
        print(obj, status1)
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


# Automatic Data Creation on the basis of data received by the api
@api_view(['POST'])
def DocumentViewSet(request):
    permission_classes=(IsAuthenticated,)
    params=request.data
    try:
        obj=Document.objects.create(
        owner=request.user,
        type=params['type'],
        source_type=params['source_type'],
        source_id=params['source_id'],
        input_meta_data=params['input_meta_data']
        )

        obj.save()
        serializer= DocumentSerializer(obj)
        return Response({'message':"Successfully Saved Data", "details":serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'message':"Error", "error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    obj.save()
