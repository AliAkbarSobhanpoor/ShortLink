from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserStepOne.as_view(), name='user-register'),
    path('register/activate/', views.RegisterUserStepTwo.as_view(), name='user-activate'),
]
