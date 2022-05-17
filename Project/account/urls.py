from django.urls import path
from account.views import UserRegistrationView, UserLoginView, BookDetail

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
   path('bk/', BookDetail.as_view()),
]
