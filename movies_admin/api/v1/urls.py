from api.v1.views import MoviesAPIView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r"movies", MoviesAPIView, basename="movies")

urlpatterns = [
    path("", include(router.urls)),
]
