from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.views import MoviesAPIView

router = DefaultRouter()

router.register(r"movies", MoviesAPIView, basename="movies")

urlpatterns = [
    path("", include(router.urls)),
]
