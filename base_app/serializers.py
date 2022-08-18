from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError


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

    # def create(self, validated_data):
    #     payment = validated_data['payment']
    #
    #     student = StudentSerializer(data=validated_data.pop('student'))
    #     student_wallet = student.initial_data['wallet']
    #     student_contract_summ = student.initial_data['contract_summ']
    #
    #     sponsor = SponsorSerializer(data=validated_data.pop('sponsor'))
    #     sponsor_wallet = sponsor.initial_data['wallet']
    #     if payment > sponsor_wallet:
    #         raise ValidationError(detail='Sponsorning puli yetarlimas')
    #     sponsor_wallet -= payment
    #     if sponsor.is_valid():
    #         sp = sponsor.save(user=self.context['request'].user)
    #     if student.is_valid():
    #         st = student.save(user=self.context['request'].user)
    #     contract = models.Contract.objects.create(**validated_data, sponsor=sp, student=st,
    #                                               user=self.context['request'].user)
    #     return contract

    class Meta:
        model = models.Contract
        fields = ('id', 'student', 'sponsor', 'payment', 'date')
