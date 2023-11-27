from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django_currentuser.middleware import get_current_user
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .serializers import UserSerializer, GroupSerializer, AuthorSerializer, BookSerializer
from .models import Author, Book


def api_token_view(request):
    token, created = Token.objects.get_or_create(user=get_current_user())
    return render(request, 'bookshelfapi/api_token.html', {'token': token})


class CustomTokenView(ObtainAuthToken):
    def get(self, request, *args, **kwargs) -> Response:
        token, created = Token.objects.get_or_create(user=get_current_user())
        return Response({'token': token.key})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
