from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import CustomUser
from .serializers import CustomUserSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def retrieve(self, request, pk):
        user = CustomUser.objects.filter(pk=pk)
        serializer = CustomUserSerializer(user, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        saved_user = CustomUser.get_manageable_object_or_404(request.user, pk=pk)
        serializer = CustomUserSerializer(instance=saved_user, partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk):
        saved_user = CustomUser.get_manageable_object_or_404(request.user, pk=pk)
        serializer = CustomUserSerializer(instance=saved_user, partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        saved_user = CustomUser.get_manageable_object_or_404(request.user, pk=pk)
        saved_user.delete()
        return Response({"User '{}' deleted".format(pk)})

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

