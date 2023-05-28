from django.urls import path
from . import views
from .views import ImageCreationView, ImageListView, ImageDetailView, ImageRankingView

app_name = 'images'

urlpatterns = [

    path('', ImageListView.as_view(), name='list'),
    path('ranking/', ImageRankingView.as_view(), name='ranking'),
    path('create/', ImageCreationView.as_view(), name='create'),
    path('detail/<int:id>/<slug:slug>/', ImageDetailView.as_view(), name='detail'),
    path('like/', views.image_like, name='like'),

]