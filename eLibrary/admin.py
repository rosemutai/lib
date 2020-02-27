from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Member)
admin.site.register(Reviews)
admin.site.register(Borrower)
