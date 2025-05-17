from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register_view, name='register'),  
    path('login/', views.login_view, name='login'),   
    path('logout/', views.logout_view, name='logout'),  
    path('profile/<int:pk>/', views.user_profile_view, name='user_profile'),  
    path('profile/update/<int:pk>/', views.update_profile_view, name='update_profile'),
]
