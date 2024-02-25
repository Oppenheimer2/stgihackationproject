from django.urls import path

from . import views

urlpatterns = [
    path("count/", views.count),
    path("mean/", views.mean),
    path("median/", views.median),
    path("psalary/", views.percentile),
]
