from django.urls import path
from .views import StatistikaView, WorkerView

urlpatterns = [
    path('stat/', StatistikaView.as_view()),
    path('worker/', WorkerView.as_view()),
]
