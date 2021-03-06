from django.db import models
from _datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=50)
    email=models.CharField(max_length=60)
    password=models.CharField(max_length=100)
    postcode=models.CharField(max_length=50)

    def __str__(self):
        return self.username

class GroupOfCategory(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Category(models.Model):
    group = models.ForeignKey(GroupOfCategory, null= True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, default='', blank=True)
    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    edition = models.CharField(max_length=25)
    ISBN = models.CharField(primary_key=True, max_length=20)
    description = models.CharField(max_length=50, default=" ")
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    book_img = models.ImageField(default='')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.book_name

class Stationery(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    slug = models.SlugField(default="", unique=True)
    item_img = models.ImageField(default='', upload_to='stationaries_images')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("web:stationeries_view", kwargs={
    #         'slug': self.slug
    #     })
    #
    # def get_add_to_cart_url(self):
    #     return reverse("web:add-to-cart", kwargs={
    #         'slug': self.slug
    #     })


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # stationery = models.ForeignKey(Stationery, on_delete=models.CASCADE)
    ISBN =models.CharField(max_length=20)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    name = models.CharField(max_length= 50)
    price=models.IntegerField(default=5)
    date= models.DateTimeField(default=datetime.now())
    quantity = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    first_name = models.CharField(max_length=20, default='', null=False, blank=False)
    last_name = models.CharField(max_length=20, default='', null=False, blank=False)
    email = models.EmailField(default='')
    location = models.CharField(max_length=20, default='')
    phone = models.IntegerField(default='')
    Description = models.TextField(max_length=255, blank=True)
    payment_status = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.first_name

    def get_total_cost(self):
        return sum(book.get_cost() for book in self.cart.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    books = models.ForeignKey(Book, on_delete=models.CASCADE)
    # stationery = models.ForeignKey(Stationery, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (self.id)

    def get_cost(self):
        return self.price * self.quantity



class GuestSession(models.Model):
    guest_id=models.IntegerField()


class GuestSession(models.Model):
    guest_id=models.IntegerField()

class Guest(models.Model):
    guest_id=models.IntegerField()
    ISBN=models.CharField(max_length=20)
    price=models.IntegerField()
    paid=models.BooleanField(default=False)
    quantity=models.IntegerField(default=1)


class ShopApplication(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        shopName = models.CharField(max_length=100)
        description = models.CharField(max_length=250)
        accept = models.BooleanField(default=False)
        cancel = models.BooleanField(default=False)
        timestamp = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return (self.shopName)

class bookshop(models.Model):
        book = models.ForeignKey(Book, on_delete=models.CASCADE)
        shop = models.ForeignKey(ShopApplication, on_delete=models.CASCADE)
        timestamp = models.DateTimeField(auto_now_add=True)
        def __str__(self):
            return (self.shop)



class BookLists(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        phone = models.IntegerField(default='')
        email = models.EmailField(default='')
        list_img = models.ImageField(default='')
        timestamp = models.DateTimeField(auto_now_add=True)
        checkout_request_id = models.CharField(max_length=250,default='')
        transaction_initiated = models.BooleanField(default=False)
        paid = models.BooleanField(default=False)

        def __str__(self):
            return self.email

class BookListsItems(models.Model):
        book = models.ForeignKey(Book, on_delete=models.CASCADE)
        booklist = models.ForeignKey(BookLists, on_delete=models.CASCADE)
        price = models.IntegerField(default=5)
        quantity = models.IntegerField(default=0)
        timestamp = models.DateTimeField(auto_now_add=True)



class Pen(models.Model):
    serial_number = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=20)
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    item_img = models.ImageField(default='')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.type

class ExerciseBook(models.Model):
    name = models.CharField(max_length=50, default='')
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    item_img = models.ImageField(default='')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Art(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    item_img = models.ImageField(default='')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Sport(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    item_img = models.ImageField(default='')
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

CATEGORY_CHOICES = (
    ('F', 'Fiction'),
    ('SCI', 'Sciences'),
    ('ROM', 'Romantic'),
    ('MYST', 'Mysteries'),
    ('HIST', 'Historical'),
    ('DET', 'Detective'),

)


class Novel(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    in_stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    slug = models.SlugField(unique=True, default='')
    description = models.TextField(default='')
    image = models.ImageField(upload_to='novels')

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Novel.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("web:novel", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("web:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("web:remove_from_cart", kwargs={
            'slug': self.slug
        })

