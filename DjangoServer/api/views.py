from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(["GET"])
def test_api(request):
    data = {"message": "Hello from Django!"}
    return Response(data)