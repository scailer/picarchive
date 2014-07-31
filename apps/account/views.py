# -*- coding:utf-8 -*-

from django.contrib.auth import login, logout

from rest_framework import views, permissions, status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.rest.auth.serializers import (LoginSerializer,
                                         SetPasswordSerializer,
                                         PasswordChangeSerializer)

from . import models
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    model = models.User
    model_serializer_class = serializers.UserSerializer
    serializer_class = serializers.UserSerializer

    @action(serializer_class=SetPasswordSerializer)
    def set_password(self, request, pk=None):
        if not request.user.is_staff:
            return Response(None, status=status.HTTP_403_FORBIDDEN)
        return self.update(request, partial=True)

    @action(serializer_class=PasswordChangeSerializer)
    def change_password(self, request, pk=None):
        return self.update(request, partial=True)


class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer


class LoginView(generics.GenericAPIView):
    """
        POST:    {"username":"admin", "password":"31415"} -> user data
    """
    serializer_class = LoginSerializer

    def get(self, request, format=None):
        if request.user.is_authenticated():
            return Response(serializers.UserSerializer(request.user).data,
                            status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        serializer = self.get_serializer_class()(data=request.DATA)

        if serializer.is_valid():
            # Okay, security checks complete. Log the user in.
            user = serializer.get_user()
            login(request, user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return Response(serializers.UserSerializer(user).data,
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    """
        POST: {} -> None
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kw):
        logout(request)
        return Response()
