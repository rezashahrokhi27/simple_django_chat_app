from django.urls import path
from django.contrib.auth import views

from .views import room, index

urlpatterns = [
    path("", index, name="index"),
    path("<str:roomname>/", room, name="room"),
    path('login/', views.LoginView.as_view(), name='login')
]