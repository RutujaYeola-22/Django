from django.db import models

# Create your models here.
class Category(models.Model):
    cname  = models.CharField(max_length = 20)
    class Meta:
        db_table = "Category"

    def __str__(self):
        return self.cname


class Cake(models.Model):
    cake_name = models.CharField(max_length = 20)
    price  = models.FloatField(default=200)
    description = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    image_url = models.ImageField(default = "abc.jpg",upload_to="media/Images/")
    cat_id = models.ForeignKey("Category",on_delete = models.CASCADE)

    class Meta:
        db_table = "Cake"


