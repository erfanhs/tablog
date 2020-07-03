from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django import forms
from .models import Post


User = get_user_model()


class UserCreateForm(UserCreationForm):

	email = forms.EmailField(required=True, label='Email address')

	class meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def __init__(self, *args, **kwargs):

		super(UserCreateForm, self).__init__(*args, **kwargs)

		for fieldname in self.fields:
			field = self.fields[fieldname]
			field.help_text = None
			field.widget.attrs['placeholder'] = field.label
			field.label = ''
			self.fields[fieldname] = field

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		user.is_active = False
		if commit:
			user.save()
		return user



class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['subject', 'content', 'image']




