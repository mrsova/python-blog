import os
from django.db import models
from PIL import Image
# Image.LOAD_TRUNCATED_IMAGES = True
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)    



class Post(models.Model):
    class Meta:
        ordering = ["-updated"]

    title = models.CharField(max_length=255, verbose_name=u"Заголовок")
    image = models.ImageField(
            upload_to=upload_location,
            null=True,
            blank=True,
            verbose_name=u"Изображение"
            )
    photo_medium = models.CharField(max_length=255, blank=True,null=True)
    photo_thumb = models.CharField(max_length=255, blank=True,null=True)
    content = models.TextField(verbose_name=u"Содержание")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u"Дата обновления")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u"Дата создания")

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        #reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])
        return reverse("posts:detail", kwargs={"id":self.id})

    def save(self):         
            try:
                 old_obj = Post.objects.get(id=self.id)
                 if old_obj.image.path != self.image.path:
                     old_obj.image.delete(save=False)                 
            except: 
                pass 

            sizes = {'thumbnail': {'height': 100, 'width': 100}, 'medium': {'height': 300, 'width': 300},}
            super(Post, self).save()

            image_path = str(self.image.path)  # Путь к оригинальному изображению
            image_url = str(self.image.url)  # Путь url

            im = Image.open(image_path)  # Открываем оригинальное изображение     
            # pull a few variables out of that full path
            extension = image_url.rsplit('.', 1)[1]  # Получаем расширение файла
            # filename = image_url.rsplit('/', 1)[2].rsplit('.', 1)[0]  # получаем имя файла
            filename = image_url.rsplit('/', 1)[1].rsplit('.', 1)[0]  # получаем имя файла
            fullpath = image_path.rsplit('\\', 1)[0] # получаем путь без фала
            
            fullu = image_url.rsplit('/', 1)[0]
            # Проверяем расширение
            if extension not in ['jpg', 'jpeg', 'gif', 'png']: sys.exit()
            
            # create medium image
            im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
            medname = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height'])+"."+ extension
            path_save = fullpath + '/' + medname
            path_u = fullu + '/' + medname
            im.save(path_save)
            self.photo_medium = path_u
           
            # create thumbnail
            im.thumbnail((sizes['thumbnail']['width'], sizes['thumbnail']['height']), Image.ANTIALIAS)
            thumbname = filename + "_" + str(sizes['thumbnail']['width']) + "x" + str(sizes['thumbnail']['height'])+"."+extension
            path_save = fullpath + '/' + thumbname
            path_u =fullu + '/' + thumbname
            im.save(path_save)
            self.photo_thumb = path_u
            
            super(Post, self).save()

            
