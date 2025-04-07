from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *


app_name  ="taskapp"

urlpatterns = [
    
    path('', LoginPage.as_view(), name='LoginPage'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('LoginUser/', LoginUser.as_view(), name='LoginUser'),
    path('IndexPage/', IndexPage.as_view(), name='IndexPage'),
    path('UsersTemplateView/', UsersTemplateView.as_view(), name='UsersTemplateView'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('SuperViewAdmin/', SuperViewAdmin.as_view(), name='SuperViewAdmin'),
    path('SuperViewUser/', SuperViewUser.as_view(), name='SuperViewUser'),
    path('SuperCreateTask/', SuperCreateTask.as_view(), name='SuperCreateTask'),
    path('AdminCreateTask/', AdminCreateTask.as_view(), name='AdminCreateTask'),
    path('AdminViewReport/', AdminViewReport.as_view(), name='AdminViewReport'),
    path('SuperDeleteUser/', SuperDeleteUser.as_view(), name='SuperDeleteUser'),
    path('UsersTaskView/', UsersTaskView.as_view(), name='UsersTaskView'),
]
