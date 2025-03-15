from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'
urlpatterns = [
    path('register/', views.register_view, name='register'),  
    path('login/', views.login_view, name='login'),   
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),  
    path('profile/<int:pk>/', views.user_profile_view, name='user_profile'),  
    path('profile/update/<int:pk>/', views.update_profile_view, name='update_profile'),
]