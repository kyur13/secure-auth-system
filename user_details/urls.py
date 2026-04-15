from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('profile/', ProfileAPI.as_view()),
    path('change-password/', ChangePasswordAPI.as_view()),
    path('sample/', SampleAPI.as_view()),
]