from django import forms
from .models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g, xyz01'
                }
            ),
            'fullname': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g, abc xyz'
                }
            ),
            'emailId': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g, abc@domain.com'
                }
            ),
            'bio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'About me...'
                }
            ),
            'password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g, aBc!@#$123'
                }
            ),
        }


class AuthorLoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g, xyz01'}))
    password = forms.CharField(max_length=75, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'e.g, aBc!@#$123'}))


class WriteBlogForm(forms.Form):
    title = forms.CharField(max_length=350, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of blog.'}))
    excerpt = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Excerpt of blog.'}))
    blog = forms.CharField(max_length=10000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write.....', 'rows': 20}))


class ForgotPassword(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g, xyz01'}))
    email = forms.CharField(max_length=250, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'e.g, abc@domain.com'}))
    password = forms.CharField(max_length=75, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'e.g, aBc!@#$123'}))
    confirm_password = forms.CharField(max_length=75, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'e.g, aBc!@#$123'}))


class CommentForm(forms.Form):
    readerName = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    readerEmail = forms.EmailField(max_length=250, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    readerComment = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...', 'rows': 5}))