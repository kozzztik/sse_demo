from django.urls import path
from sse_demo import views


urlpatterns = [
    path(r'', views.HomeView.as_view()),
    path(r'sse/', views.SSEAPI.as_view())
]
