from django.urls import path

from company import views

urlpatterns = [
    path('about/', views.AboutView.as_view()),
    path('contact/', views.ContactView.as_view()),
]
