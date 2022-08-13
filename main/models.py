from django.db import models
from django.contrib.auth.models import User
from hashlib import sha1

# class Users(models.Model):
#     email = models.TextField()
#     password = models.CharField(max_length=60)
#     status = models.CharField(max_length=5)
#     activate = models.IntegerField()
#     user_token = models.TextField()
#     user_information = models.ForeignKey('User_Information', on_delete=models.CASCADE, null=True)


# class User_Information(models.Model):
#     name = models.CharField(max_length=40)
#     surname = models.CharField(max_length=40)
#     patronymic = models.CharField(max_length=40)
#     birthday = models.DateField()


class Comment(models.Model):
    parent_id = models.BigIntegerField()
    comments_author = models.TextField()
    comment_text = models.TextField()
    date_posted = models.DateTimeField()
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'


class Article(models.Model):
    title = models.CharField(max_length=500, verbose_name='Название')
    text = models.TextField(verbose_name='Содержание')
    title_image = models.ImageField(upload_to="article_photo/", verbose_name='Картинка')
    publication_date = models.DateField(verbose_name='Дата публикации')

    def comments_length(self):
        return len(Comment.objects.filter(article_id=self.pk).all())

    class Meta:
        verbose_name = 'статью'
        verbose_name_plural = 'Статьи'