from django.urls import path

from blog import views

urlpatterns = [
    path('posts/', views.PostsView.as_view()),
    path('posts/search/', views.SearchPostView.as_view()),
    path('posts/date/<str:date_post>/', views.FilterDatePostsView.as_view()),
    path('posts/<slug:slug>/', views.PostDetailView.as_view()),
    path('add-comment/', views.AddCommentView.as_view()),
    path('categories/', views.CategoryListView.as_view()),
    path('videos/', views.VideoListView.as_view()),
]
