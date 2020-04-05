from .models import Document
from rest_framework import status
from django.contrib.auth.models import User
from .get_meta_data import create_input_meta_data

def add_data_or_400(request):
    params=request.data
    if('document' in request.FILES):
        meta_data=create_input_meta_data(request)
        print(meta_data)

        obj=Document.objects.create(
        owner=request.user,
        type=params['type'],
        source_type=params['source_type'],
        source_id=params['source_id'],
        input_meta_data=meta_data
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
