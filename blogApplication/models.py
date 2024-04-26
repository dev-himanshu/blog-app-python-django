from django.db import models

# Create your models here.


class Author(models.Model):
    username = models.CharField(max_length=50, primary_key=True, blank=False, null=False, unique=True)
    fullname = models.CharField(max_length=250, blank=False, null=False)
    emailId = models.EmailField(max_length=250, blank=False, null=False, unique=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=75, blank=False, null=False)

    def __str__(self):
        return self.username


class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=350, blank=False, null=False)
    excerpt = models.CharField(max_length=1000)
    blog = models.CharField(max_length=10000)
    blogDateTime = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    readerName = models.CharField(max_length=250)
    readerEmail = models.EmailField(max_length=250)
    readerComment = models.CharField(max_length=5000)
    commentDateTime = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.readerName
