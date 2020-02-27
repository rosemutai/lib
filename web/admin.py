from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(GroupOfCategory)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShopApplication)
admin.site.register(bookshop)
admin.site.register(BookLists)
admin.site.register(BookListsItems)
admin.site.register(Stationery)
admin.site.register(ExerciseBook)
admin.site.register(Pen)
admin.site.register(Art)
admin.site.register(Sport)