from django.urls import path

from .views import api_token_view

urlpatterns = [
    path('api-token', api_token_view, name='api')
]
