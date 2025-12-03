from django.urls import path
from app import views


urlpatterns = [
    path("retriever/", views.RetrieverAPIView.as_view(), name="retreiver")
]