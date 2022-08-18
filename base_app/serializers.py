from rest_framework import serializers
from . import models


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sponsor
        fields = ('id', 'name', 'phone', 'wallet', 'type_sponsor', 'status', 'organization_name', 'datesp')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ('id', 'full_name', 'phone', 'otm', 'type_student', 'contract_summ', 'wallet', 'datest')


class ContractSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    sponsor = SponsorSerializer(read_only=True)

    class Meta:
        model = models.Contract
        fields = ('id', 'student', 'sponsor', 'payment', 'date')
