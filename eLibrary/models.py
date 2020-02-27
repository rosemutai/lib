from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return  self.name

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    pic=models.ImageField(blank=True, null=True, upload_to='book_image')

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m',
                              help_text='Book Availability')
    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return   self.book.title

class Member(models.Model):
    member_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=10)
    location = models.CharField(max_length=20)
    total_books_due=models.IntegerField(default=0)
    pic=models.ImageField(blank=True, upload_to='profile_image')

    def __str__(self):
        return str(self.username)

class Borrower(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.member.first_name +self.member.last_name+" borrowed "+self.book.title

class Reviews(models.Model):
    review=models.CharField(max_length=100,default="none")
    book=models.ForeignKey(BookInstance,on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    CHOICES = (
        ('0', '0'),
        ('.5', '.5'),
        ('1', '1'),
        ('1.5', '1.5'),
        ('2', '2'),
        ('2.5', '2.5'),
        ('3', '3'),
        ('3.5', '3.5'),
        ('4', '4'),
        ('4.5', '4.5'),
        ('5', '5'),
    )

    rating=models.CharField(max_length=3, choices=CHOICES, default='2')