from django.urls import path

from users import views

urlpatterns = [
    path('<int:pk>/', views.AuthorDetailView.as_view()),
]
