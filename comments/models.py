from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
# Create your models here.


class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs


class Comment(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, default=1) 
    #post      = models.ForeignKey(Post)
    #связка по ключу
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentManager()
    content   = models.TextField(verbose_name=u"Комментарий")
    timestamp = models.DateTimeField(auto_now=True, verbose_name=u"Дата создания")
    
    def __str__(self):
        return str(self.user.username)