from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.home_view, name='home'), 
    path('post/<int:pk>/', views.post_view, name='post'),  
    path('create/', views.create_post_view, name='create_post'), 
    path('categories/', views.category_view, name='category'), 
    path('categories/<str:category>/', views.category_view, name='category_posts'),  
    path('update/<int:pk>/', views.update_post_view, name='update_post'),  
    path('delete/<int:pk>/', views.delete_post_view, name='delete_post'),
    path('message/update/<int:pk>/', views.update_message_view, name='update_message'),  
    path('delete-message/<int:pk>/', views.delete_message, name='delete_message'),  
   
]