from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta



class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id
    
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
        ('roman', 'Roman'),
        ]
    name=models.CharField(max_length=30)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    enrollment = models.ForeignKey(StudentExtra, on_delete=models.CASCADE, related_name='issued_books')
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issued_instances')
    issuedate = models.DateField(auto_now_add=True)  # auto_now_add для даты выдачи
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return f"{self.enrollment.get_name} - {self.isbn.name}"

    
    class Meta:
        verbose_name = 'Выпущенная книга'
        verbose_name_plural = 'Выпущенные книги'

