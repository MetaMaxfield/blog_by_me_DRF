from django.urls import path

from company import views

urlpatterns = [
    # path('about/', views.AboutView.as_view()),
    path('about/', views.AboutViewSet.as_view({'get': 'retrieve'})),
    path('contact/', views.ContactView.as_view()),
]
