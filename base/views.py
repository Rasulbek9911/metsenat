from django.shortcuts import render
from rest_framework import generics
from .serializers import CompanySerializer, VakancySerializer, WorkerSerializer
from .models import Company, Vakancy, Worker, Category
from django.db.models import Count, F, Sum, Avg, Max, Min
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models


# Create your views here.


class StatistikaView(APIView):
    def get(self, request):
        company_count = Company.objects.all().count()
        vakancy_count = Vakancy.objects.all().count()
        worker_count = Worker.objects.all().count()
        data = {
            "company_count": company_count,
            "vakancy_count": vakancy_count,
            "worker_count": worker_count
        }
        return Response(data=data)


class WorkerView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = WorkerSerializer

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.annotate(
            salary=models.Case(
                models.When(Max('worker__to_s') / Min('worker__from_s') > 2,
                            then=f"{Min('worker__from_s') + (Min('worker__from_s') + Max('worker__to_s')) / 2}-{Min('worker__to_s') + (Min('worker__from_s') + Max('worker__to_s')) / 2}"),
                models.When(Max('worker__to_s') / Min('worker__from_s') < 2,
                            then=f"{(Min('worker__from_s') + Max('worker__to_s')) / 2}")
            )
        )
        return queryset


