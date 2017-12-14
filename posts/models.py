import os
from django.db import models
from django.conf import settings
from PIL import Image
import shutil
from django.contrib.contenttypes.models import ContentType
Image.LOAD_TRUNCATED_IMAGES = True
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils .text import slugify
from unidecode import unidecode
from django.utils import timezone



# Create your models here.
flag = False

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    print(instance.id)
    return "%s/%s" % (instance.id, filename)    


class Post(models.Model):
    class Meta:
        ordering = ["-updated"]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)    
    title = models.CharField(max_length=255, verbose_name=u"Заголовок")
    slug = models.SlugField(unique=True, blank=True)
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
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u"Дата обновления")
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u"Дата создания")
    
    
    objects = PostManager()

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        #reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])
        return reverse("posts:detail", kwargs={"slug":self.slug}) #Находит паттерн и подставляет

    
    #Переопределяем сохранение чтобы получить id
    def save(self, *args, **kwargs):
        if self.id is None:
            saved_image = self.image
            self.image = None
            super(Post, self).save(*args, **kwargs)
            self.image = saved_image
            # kwargs.pop('force_insert')

        super(Post, self).save(*args, **kwargs)

#Удаление картинок при удалении поста
@receiver(post_delete, sender=Post)
def delete_post(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    if instance.image:
        shutil.rmtree(str(instance.image.path.rsplit('\\', 1)[0]))


def create_slug(instance, new_slug=None):
    slug = slugify(unidecode(instance.title))
    new_slug = "{0}-{1}".format(slug, instance.id)
    return new_slug

#Проверка перед сохранением поста
@receiver(pre_save, sender=Post)
def my_pre_callback(sender, instance, *args, **kwargs):
    global flag
    if instance.id:
        old = Post.objects.get(id=instance.id)
        if old.image and old.image != instance.image:
            old.image.delete(save=False)
            instance.photo_medium.delete(save=False)        
        else:
            flag = True
    else:
        flag = True

#После сохранения
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

   
    post_save.disconnect(my_callback, sender=sender)   
    instance.slug = create_slug(instance)
    instance.save()
    post_save.connect(my_callback, sender=sender)
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
        fullu = image_url.split('/')[2]

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
