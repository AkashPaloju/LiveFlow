from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
                return user


class Uploader(forms.Form):
    video_name = forms.CharField(label="Enter Video name : ", max_length=100)
    description = forms.CharField(label="Describe your video : ", max_length=250)
    tags = forms.CharField(label="Type your tags like (movie,series,education etc..) :",max_length=200)
    file = forms.FileField()
