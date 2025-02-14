from django.urls import include, path
from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register(r'', views.AuthorViewSet, basename='Author')

urlpatterns = [
    # path('', views.AuthorListView.as_view()),
    # path('<int:pk>/', views.AuthorDetailView.as_view()),
    path('', include(router.urls)),
]
