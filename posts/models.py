from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Заголовок")
    image = models.FileField(null=True, blank=True, verbose_name=u"Изображение")
    content = models.TextField(verbose_name=u"Содержание")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u"Дата обновления")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u"Дата создания")

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        #reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])
        return reverse("posts:detail", kwargs={"id":self.id})
        # return "/posts/%s/" %(self.id)
    
    class Meta:
        #Сортировка
        ordering = ["-updated"]
