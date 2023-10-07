from django.urls import path
from . import views


urlpatterns = [
    path('api/lessons/', views.LessonViewList.as_view(),
         name='lesson-list'),
    path('api/lessons-by-product/', views.LessonListByProduct.as_view(),
         name='lessons-by-product'),
    path('api/product-statistics/', views.ProductStatistics.as_view(),
         name='product-statistics'),
]
