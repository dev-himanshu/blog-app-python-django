from django.urls import path
from .views import index, specificBlog, signup, authorLogin, authorLogout, home, writeBlog, editBlog
from .views import forgotPassword, CommentView, profile, editProfile, settings

urlpatterns = [
    path('', index, name="IndexPage"),
    path('login/', authorLogin, name="loginPage"),
    path('signup/', signup, name="signupPage"),
    path('post/<int:post_id>/', specificBlog, name="SpecificPostPage"),
    path('home/', home, name="homePage"),
    path('write/', writeBlog, name="writeBlogPage"),
    path('home/edit/<int:post_id>/', editBlog, name="editBlogPage"),
    path('logout/', authorLogout, name="logoutPage"),
    path('profile/', profile, name="profilePage"),
    path('edit/', editProfile, name="profileEditPage"),
    path('setting/', settings, name="settingAuthor"),
    path('passwordchangerequest/', forgotPassword, name="passwordChangeRequest"),
    path("comment_api/", CommentView.as_view(), name="commentAPI"),
]
# API url --> http://127.0.0.1:8000/comment_api/
