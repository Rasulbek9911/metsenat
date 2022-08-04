from rest_framework import serializers
from .models import Company, Vakancy, Worker


class CompanySerializer(serializers.ModelSerializer):
    company_count = serializers.IntegerField()

    class Meta:
        model = Company
        fields = ('id', 'title', 'vakancy', 'company_count')


class VakancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vakancy
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'
