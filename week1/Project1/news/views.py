from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from news.models import Stuff, StuffStockDetails
from news.serializers import StuffSerializer, StuffListSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import Http404


@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@api_view(['POST'])
def logout(request):
    request.auth.delete()
    return Response(status=status.HTTP_200_OK)


class Stuff_List(generics.ListCreateAPIView):
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# class StuffStockDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Stuff.objects.all()
#     serializer_class = StuffSerializer


class StuffStockDetails(APIView):
    def get_object(self, pk):
        try:
            return Stuff.objects.get(id=pk)
        except Stuff.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        taski = self.get_object(pk)
        serializer = StuffListSerializer(taski)
        return Response(serializer.data)

    def put(self, request, pk):
        taski = self.get_object(pk)
        serializer = StuffListSerializer(instance=taski, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)

    def delete(self, request, pk):
        taski = self.get_object(pk)
        taski.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
