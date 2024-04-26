from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import AuthorForm, AuthorLoginForm, WriteBlogForm, ForgotPassword, CommentForm
from .models import Blog, Author, Comments
from .serializer import CommentSerializer
# Create your views here.


def index(request):
    all_blogs = Blog.objects.all().order_by('-blogDateTime')
    paginator = Paginator(all_blogs, 4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'blogApplication/index.html', context={'title': "Landing Page", 'blogs': page_object, 'name': request.user.username})


def specificBlog(request, post_id):
    data = Blog.objects.get(id=post_id)
    comments = Comments.objects.filter(blog=data).order_by('-commentDateTime')
    paginator = Paginator(comments, 1)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('readerName')
            email = form.cleaned_data.get('readerEmail')
            comment = form.cleaned_data.get('readerComment')
            new_comment = Comments(blog=data, readerName=name, readerEmail=email, readerComment=comment)
            new_comment.save()
            comments = Comments.objects.filter(blog=data).order_by('-commentDateTime')
            paginator = Paginator(comments, 1)
            page_number = request.GET.get('page')
            page_object = paginator.get_page(page_number)
            form = CommentForm()
            return render(request, 'blogApplication/specificPost.html',
                          {'title': "Post", 'blog_data': data, 'name': request.user.username, 'commentForm': form,
                           'all_comments': page_object})
    return render(request, 'blogApplication/specificPost.html', {'title': "Post", 'blog_data': data, 'name': request.user.username, 'commentForm': form, 'all_comments': page_object})


def signup(request):
    form = AuthorForm()
    if request.user.is_authenticated:
        return redirect('homePage')
    else:
        if request.method == "POST":
            form = AuthorForm(request.POST)
            if form.is_valid():
                user_exist = User.objects.filter(username=form.cleaned_data.get('username'))
                if user_exist:
                    messages.error(request, message="Choose another username!!!")
                    return redirect('signupPage')
                else:
                    user_exist = User.objects.filter(email=form.cleaned_data.get('emailId'))
                    if user_exist:
                        messages.error(request, message="Email already used!!!")
                        return redirect('signupPage')
                    else:
                        form.save()
                        name = form.cleaned_data.get('fullname')
                        user = User(username=form.cleaned_data.get('username'), email=form.cleaned_data.get('emailId'),
                                    password=make_password(form.cleaned_data.get('password')))
                        user.save()
                        message = f"{name} registered successfully!!!"
                        messages.success(request, message=message)
                        return redirect('loginPage')
            else:
                messages.error(request, message="username/email already exist!!!")
                return redirect('signupPage')
        return render(request, 'blogApplication/signup.html', {'title': "Sign Up", 'form': form, 'user': request.user.username})


def authorLogin(request):
    loginForm = AuthorLoginForm()
    if request.user.is_authenticated:
        return redirect('homePage')
    else:
        if request.method == "POST":
            loginForm = AuthorLoginForm(request.POST)
            if loginForm.is_valid():
                username = loginForm.cleaned_data.get('username')
                pwd = loginForm.cleaned_data.get('password')
                user = authenticate(request, username=username, password=pwd)
                if user is not None:
                    login(request, user=user)
                    messages.success(request, message=f"Welcome {user} !!!")
                    return redirect('homePage')
                else:
                    messages.error(request, message="Invalid username/password!!!")
                    return redirect('loginPage')
    return render(request, 'blogApplication/login.html', {'title': "Log In", 'loginForm': loginForm})


@login_required(login_url='loginPage')
def authorLogout(request):
    logout(request)
    return render(request, 'blogApplication/logout.html', {'title': "Log Out"})


@login_required(login_url='loginPage')
def home(request):
    all_blogs = Blog.objects.filter(author=request.user.username).order_by('-blogDateTime')
    paginator = Paginator(all_blogs, 4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'blogApplication/home.html', {'title': "Home", 'blogs': page_object, 'user': request.user.username})


@login_required(login_url='loginPage')
def writeBlog(request):
    blog_form = WriteBlogForm()
    if request.method == "POST":
        blog_form = WriteBlogForm(request.POST)
        if blog_form.is_valid():
            user_name = request.user.username
            author = Author.objects.get(username=user_name)
            blog = Blog(author=author, title=blog_form.cleaned_data.get("title"),
                        excerpt=blog_form.cleaned_data.get("excerpt"), blog=blog_form.cleaned_data.get("blog"))
            blog.save()
            messages.success(request, message=f"Blog: {blog_form.cleaned_data.get('title')} posted successfully!!!")
            return redirect('homePage')
    return render(request, 'blogApplication/writeblog.html', {'title': "Write Blog", 'blog_form': blog_form, 'user': request.user.username})


@login_required(login_url='loginPage')
def editBlog(request, post_id):
    data = Blog.objects.get(id=post_id)
    if request.method == "POST":
        title = request.POST.get('inputTitle')
        excerpt = request.POST.get('inputExcerpt')
        blog = request.POST.get('inputBlog')
        update_blog = Blog.objects.get(id=post_id)
        update_blog.title = title
        update_blog.excerpt = excerpt
        update_blog.blog = blog
        update_blog.save()
        messages.success(request, message="Blog updated successfully!!!")
        return redirect('homePage')
    return render(request, 'blogApplication/editpost.html', {'title': "Edit Blog", 'blog_data': data, 'user': request.user.username})


@login_required(login_url='loginPage')
def profile(request):
    user_name = request.user.username
    author = Author.objects.get(username=user_name)
    total_blog = Blog.objects.filter(author=author).count()
    return render(request, 'blogApplication/profile.html', {'title': f"{author.fullname}", 'profile': author, 'user': request.user.username, 'total': total_blog})


@login_required(login_url='loginPage')
def editProfile(request):
    user_name = request.user.username
    author = Author.objects.get(username=user_name)
    if request.method == "POST":
        fullName = request.POST.get('inputFullName')
        email = request.POST.get('inputEmail')
        bio = request.POST.get('inputBio')
        author.fullname = fullName
        author.emailId = email
        author.bio = bio
        author.save()
        messages.success(request, message="Profile Updated Successfully!!!")
        return redirect('homePage')
    return render(request, 'blogApplication/editProfile.html', {'title': f"{author.fullname}", 'profile': author, 'user': request.user.username})


@login_required(login_url='loginPage')
def settings(request):
    user_name = request.user.username
    author = Author.objects.get(username=user_name)
    if request.method == "POST":
        oldPassword = request.POST.get('inputOldPassword')
        newPassword = request.POST.get('inputNewPassword')
        confirmPassword = request.POST.get('inputConfirmPassword')
        if oldPassword != author.password:
            messages.error(request, message="old password is not correct.")
            return redirect('settingAuthor')
        else:
            if newPassword != confirmPassword:
                messages.error(request, message="new password and confirm password is not same.")
                return redirect('settingAuthor')
            else:
                author.password = newPassword
                user = User.objects.get(username=author.username)
                user.password = make_password(newPassword)
                user.save()
                author.save()
                messages.error(request, message="password changed successfully!!!")
                return redirect('profilePage')
    return render(request, 'blogApplication/settings.html', {'title': f"{author.fullname}", 'user': request.user.username})


def forgotPassword(request):
    forgotPasswordForm = ForgotPassword()
    if request.method == "POST":
        forgotPasswordForm = ForgotPassword(request.POST)
        if forgotPasswordForm.is_valid():
            username = forgotPasswordForm.cleaned_data.get('username')
            email = forgotPasswordForm.cleaned_data.get('email')
            pwd = forgotPasswordForm.cleaned_data.get('password')
            c_pwd = forgotPasswordForm.cleaned_data.get('confirm_password')
            try:
                author = Author.objects.get(username=username, emailId=email)
                if author:
                    if pwd != c_pwd:
                        messages.success(request, message="Password not matched!")
                        return redirect('passwordChangeRequest')
                    else:
                        author.password = pwd
                        author.save()
                        user = User.objects.get(username=author.username)
                        user.password = make_password(pwd)
                        user.save()
                        messages.error(request, message="password changed successfully!!!")
                        return redirect('loginPage')
                else:
                    messages.success(request, message="User not exist!!!")
                    return redirect('passwordChangeRequest')
            except Author.DoesNotExist:
                messages.success(request, message="User not exist!!!")
                return redirect('passwordChangeRequest')
    return render(request, 'blogApplication/forgotPasswordOne.html', {'title': 'Change Password', 'forgotForm': forgotPasswordForm})


class CommentView(APIView):

    def get(self, request, *args, **kwargs):
        comments = Comments.objects.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data)
