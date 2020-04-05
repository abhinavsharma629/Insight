from rest_framework import serializers
from .models import Document
from django.contrib.auth.models import User


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
      model=User  # what module you are going to serialize
      fields= ('username','first_name', 'last_name')


class DocumentSerializer(serializers.ModelSerializer):
    owner=UserDetailsSerializer('owner')

    class Meta:
      model=Document  # what module you are going to serialize
      fields= ('owner','created','type','source_type','source_id','input_meta_data')
