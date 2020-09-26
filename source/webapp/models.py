from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

CATEGORY_CHOICES = (
    ('other', 'Other'),
    ('food', 'Food'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('cars', 'Cars'),
)

GRADE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    description = models.TextField(max_length=2000, verbose_name='Description', null=True, blank=True)
    category = models.CharField(max_length=50, verbose_name='Category', choices=CATEGORY_CHOICES)
    pic = models.ImageField(null=True, blank=True, upload_to='product_pics', verbose_name='Product image')

    def __str__(self):
        return f'{self.name}'

    def get_average(self):
        avg = self.review_set.aggregate(
            Avg('grade')
        )
        avg = avg.get('grade__avg')
        if avg is not None:
            return ("%.2f" % avg)
        return 0


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, \
                             related_name='reviews', verbose_name='Author')
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE, verbose_name='Product')
    text = models.TextField(max_length=1000, verbose_name='Text')
    grade = models.IntegerField(verbose_name='Grade', choices=GRADE_CHOICES)

    def __str__(self):
        return f'{self.author} for {self.product}: {self.grade}'