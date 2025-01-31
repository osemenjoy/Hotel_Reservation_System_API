from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('', UserListView.as_view(), name='user_list'),
    path('<uuid:pk>/', UserDetailView.as_view(), name='user_detail'),
]