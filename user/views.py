from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterUserSerializer


@api_view(['PUT'])
def register(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'user signed up successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)