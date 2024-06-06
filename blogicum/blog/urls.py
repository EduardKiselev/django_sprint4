from django.urls import path
from blog import views
from . import views
app_name = 'blog'

urlpatterns = [
     path('', views.index, name='index'),
     path('posts/<int:id>/', views.post_detail,
          name='post_detail'),
     path('category/<slug:category_slug>/',
          views.category_posts, name='category_posts'),
     path('profile/<slug:profile_slug>/', views.ProfileDetailView.as_view(), name='profile')
]
