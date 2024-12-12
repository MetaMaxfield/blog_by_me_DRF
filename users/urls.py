from django.urls import path

from users import views

urlpatterns = [
    path('', views.AuthorListView.as_view()),
    path('<int:pk>/', views.AuthorDetailView.as_view()),
]
