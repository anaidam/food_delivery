from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


class Category(models.Model):
    cat_name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.cat_name


class MenuItems(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()
    image       = models.ImageField(upload_to='images', blank=True, null=True)
    price       = models.DecimalField(max_digits=5, decimal_places=2)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)


    @property
    def reviews(self):
        return Reviews.objects.filter(item = self)

    def __str__(self) -> str:
        return self.name




class Carts(models.Model):
    item         = models.ForeignKey(MenuItems,on_delete=models.CASCADE)
    user         = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    options      = (
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )
    status      =models.CharField(max_length=200,choices=options,default="in-cart")
    qty         =models.PositiveIntegerField(default=0)


class Order(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    item       = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    name       = models.CharField(max_length=100)
    phone      = models.CharField(max_length=13)
    address    = models.CharField(max_length=300)

    options=(
        
        ("order-placed","order-placed"),
        ("onthe-way","onthe-way"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),
        ("return","return")
    )
    status = models.CharField(max_length=200,choices=options,default="order-placed")



class Reviews(models.Model):
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    item    = models.ForeignKey(MenuItems,on_delete=models.CASCADE)
    comment = models.CharField(max_length=240)
    date    = models.DateField(auto_now_add=True)
    rating  = models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.comment


