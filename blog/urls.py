from django.urls import path
from .views import   BlogListView , BlogCreateView, BlogUpdateView,  BlogDeleteView
from . import views


urlpatterns = [
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('', BlogListView.as_view(), name='home'),
    path('register', views.register_request, name='register'),
    
   
]