from rest_framework.serializers import ModelSerializer
from .models import Author, Blog, Comments


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['fullname']


class BlogSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['title', 'author']


class CommentSerializer(ModelSerializer):
    blog = BlogSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = ['readerName', 'readerComment', "blog"]
