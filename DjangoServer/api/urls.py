from django.urls import path
from .views import test_api,diagnose_symptoms

urlpatterns = [
    path("test/", test_api),
    path("diagnose/", diagnose_symptoms),
]