from django.urls import path
from .views import hello_world, test_api

urlpatterns = [
    path("hello/", hello_world),
    path("test/", test_api),
]