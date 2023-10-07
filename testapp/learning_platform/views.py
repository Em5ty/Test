from rest_framework import generics
from django.db.models import Count, Sum, Q
from .models import UserProductAccess, Lesson
from .serializers import LessonSerializer,  ProductSerializer


class LessonViewList(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user_product_accesses = UserProductAccess.objects.filter(
            user=self.request.user
        )
        lessons = Lesson.objects.filter(
            products__in=user_product_accesses.values('product')
        )
        return lessons


class LessonListByProduct(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        user_product_accesses = UserProductAccess.objects.filter(
            user=self.request.user, product_id=product_id
            )
        lessons = Lesson.objects.filter(
            products__in=user_product_accesses.values('product')
            )
        return lessons


class ProductStatistics(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_statistics = UserProductAccess.objects.values('product') \
            .annotate(
                num_viewed_lessons=Count('lessonview', filter=Q(
                    lessonview__is_viewed=True)
                    ),
                total_view_time=Sum('lessonview__view_time'),
                num_students=Count('user', distinct=True),
                purchase_percentage=Count('user') / Count(
                    'user', distinct=True
                    ) * 100
            )
        return product_statistics
