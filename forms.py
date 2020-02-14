from django import forms
from django.contrib.auth.models import User

class ChoreForm(forms.Form):
    pass

class NewUserForm(forms.Form):
    username = forms.CharField(label = "Username", max_length=40, required=True)
    password = forms.CharField(label = "Password", max_length=40, required=True)
    repeat_password = forms.CharField(label = "Enter password again", max_length=40, required=True)

    def clean_username(self):
        if User.objects.filter(username = self.cleaned_data["username"]):
            raise forms.ValidationError("user already exists")

    def clean(self):
        pw1 = self.cleaned_data.get("password")
        pw2 = self.cleaned_data.get("repeat_password")

        if pw1 != pw2:
            raise forms.ValidationError("passwords do not match")

class NewChoreForm(forms.Form):
    chore_description = forms.CharField(label = "Add a new chore", max_length=40, required=True)



