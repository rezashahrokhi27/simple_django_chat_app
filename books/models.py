from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()
    author = models.CharField(max_length=50)


    def get_qs(self, sort):
        qs = self.objects.order_by(sort)
        return qs