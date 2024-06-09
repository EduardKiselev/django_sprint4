from django.urls import path
from blog import views
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:pk>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/comment/',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:id>/delete_comment/<int:pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
    path('posts/<int:id>/edit_comment/<int:pk>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:id>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('profile/edit/', views.profile_update, name='edit_profile'),
    path('profile/<slug:username>/', views.profile, name='profile'),
]
