from django.urls import path
from .views import SponsorListApiView, SponsorRetrieveView, StudentListCreateView, StudentRetrieveView, DashboardView, \
    ContractListCreateView

urlpatterns = [
    path('sponsor-listCreate/', SponsorListApiView.as_view()),
    path('sponsor-retrieve/<int:pk>/', SponsorRetrieveView.as_view()),
    path('student-listCreate/', StudentListCreateView.as_view()),
    path('student-retrieve/<int:pk>/', StudentRetrieveView.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('contract-listCreate/', ContractListCreateView.as_view()),
]
