from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Заголовок")
    content = models.TextField(verbose_name=u"Содержание")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u"Дата обновления")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u"Дата создания")

    def __str__(self):
        return self.title
