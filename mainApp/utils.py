from .models import Document
from rest_framework import status
from django.contrib.auth.models import User


def add_data_or_400(request):
    params=request.data
    if('type' in params):
        obj=Document.objects.create(
        owner=request.user,
        type=params['type'] if 'source_type' in params else None,
        source_type=params['source_type'] if 'source_type' in params else None,
        source_id=params['source_id'] if 'source_type' in params else None,
        input_meta_data=params['input_meta_data'] if 'source_type' in params else None
        )
        obj.save()
        return [obj,status.HTTP_201_CREATED]
    else:
        return [None, status.HTTP_400_BAD_REQUEST]


def delete_data_or_404(request):
    params=request.data
    if(Document.objects.filter(owner=request.user, pk=params['data_id']).count()>0):
        Document.objects.get(owner=request.user, pk=params['data_id']).delete()
        return status.HTTP_200_OK
    else:
        return status.HTTP_404_NOT_FOUND
