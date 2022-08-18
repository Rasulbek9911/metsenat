from rest_framework import generics
from .models import Sponsor, Student, Contract
from .serializers import SponsorSerializer, StudentSerializer, ContractSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from helpers.pagination import CustomPagination
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


class SponsorListApiView(generics.ListCreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['datesp']
    search_fields = ['name', 'organization_name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class SponsorRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.select_related('user').all()
    serializer_class = SponsorSerializer
    permission_classes = (IsAuthenticated,)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['datest']
    search_fields = ['full_name', 'otm']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class StudentRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated,)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class DashboardView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        sponsor = Sponsor.objects.datetimes('datesp', 'month').annotate(soni=Count('id')).values('soni',
                                                                                                 'datesp__month')
        student = Student.objects.datetimes('datest', 'month').annotate(soni=Count('id')).values('soni',
                                                                                                 'datest__month')
        sponsors = []
        students = []

        def get_month(n):
            month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                     "November", "December"]
            return month[n - 1]

        for i in sponsor:
            sponsors.append(f"{get_month(i['datesp__month'])}- {i['soni']}")

        for i in student:
            students.append(f"{get_month(i['datest__month'])}- {i['soni']}")

        return Response(data={"sponsors": sponsors, "students": students})


class ContractListCreateView(generics.ListCreateAPIView):
    queryset = Contract.objects.select_related('student', 'sponsor').all()
    serializer_class = ContractSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['date']
    search_fields = ['student__full_name', 'sponsor__name']

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sponsor = Sponsor.objects.get(id=serializer.initial_data['sponsor'])
        student = Student.objects.get(id=serializer.initial_data['student'])
        payment = serializer.initial_data['payment']

        if not payment <= sponsor.wallet:
            raise ValidationError(detail="Sponsorning puli yetarlimas")
        sponsor.wallet -= payment

        if student.wallet + payment > student.contract_summ:
            raise ValidationError(
                detail=f"Bu studentga {student.contract_summ - student.wallet} gacha mablag' kirita olasiz,siz ortiqcha mablag' kiritdingiz!")
        student.wallet += payment
        student.save()
        sponsor.save()
        serializer.save(user=request.user, student=student, sponsor=sponsor)

        return Response(data=serializer.data)

    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
