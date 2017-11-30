import os
from django.db import models
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here.
flag = False

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
    # photo_medium = models.CharField(max_length=255, blank=True,null=True)
    # photo_thumb = models.CharField(max_length=255, blank=True,null=True)
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        verbose_name=u"Изображение"
        )
    photo_medium = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        verbose_name=u"Изображение среднее"
        )
    photo_thumb = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        verbose_name=u"Изображение обычное"
        )
    content = models.TextField(verbose_name=u"Содержание")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u"Дата обновления")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u"Дата создания")

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        #reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])
        return reverse("posts:detail", kwargs={"id":self.id})

@receiver(pre_save, sender=Post)
def my_pre_callback(sender, instance, *args, **kwargs):
    global flag
    old = sender.objects.get(id=instance.id) 
    if old.image and old.image != instance.image:
        pass
    else:
        flag = True

@receiver(post_save, sender=Post)
def my_callback(sender, instance, created, *args, **kwargs):
    global flag
    sizes = {
        'thumbnail':{
            'height': 100,
            'width': 100
        },
        'medium': {
            'height': 300,
            'width': 300
        }
    }  

    if instance.image and flag:
        image_path = str(instance.image.path)  # Путь к оригинальному изображению
        image_url = str(instance.image.url)  # Путь url
        # Путь до загружаемого файла
        #Дирректория в которой будет лежать файл
        fullpath = image_path.rsplit('\\', 1)[0]
     
        im = Image.open(image_path)
        #Получаем расширение        
        extension = image_url.rsplit('.', 1)[1]
        #Получаем имя 
        filename = image_url.rsplit('/', 1)[1].rsplit('.', 1)[0]
        fullu = image_url.rsplit('/', 1)[0]
        if extension not in ['jpg', 'jpeg', 'gif', 'png']: sys.exit()
        
        # # create medium image
        im.thumbnail((sizes['medium']['width'], sizes['medium']['height']), Image.ANTIALIAS)
        medname = filename + "_" + str(sizes['medium']['width']) + "x" + str(sizes['medium']['height'])+"."+ extension
        path_save = fullpath + '/' + medname
        im.save(path_save)
        
        post_save.disconnect(my_callback, sender=sender)
        
        instance.photo_medium = fullu + '/' + medname

        instance.save()
        post_save.connect(my_callback, sender=sender)
        flag = False
