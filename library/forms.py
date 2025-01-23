from django import forms
from django.contrib.auth.models import User
from . import models

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))




class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']



class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['enrollment','branch']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','isbn','author','category']



class IssuedBookForm(forms.ModelForm):
    class Meta:
        model = models.IssuedBook
        fields = ['enrollment', 'isbn']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['isbn'].queryset = models.Book.objects.all()
        self.fields['enrollment'].queryset = models.StudentExtra.objects.all()
    
