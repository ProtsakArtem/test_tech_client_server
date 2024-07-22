from django.shortcuts import render
from rest_framework import viewsets
from .models import DataRecord
from .serializers import DataRecordSerializer
# Create your views here.


class DataRecordViewSet(viewsets.ModelViewSet):
    queryset = DataRecord.objects.all()
    serializer_class = DataRecordSerializer