from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    video_link = models.URLField()
    duration = models.IntegerField()
    products = models.ManyToManyField(Product)


class UserProductAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_lessons = models.ManyToManyField(Lesson, through='LessonView')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time = models.IntegerField()
    is_viewed = models.BooleanField(default=False)
    user_product_access = models.ForeignKey(UserProductAccess,
                                            on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'lesson', 'user_product_access')
