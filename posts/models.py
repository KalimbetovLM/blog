from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
from hitcount.models import HitCountMixin,HitCount
from django.contrib.contenttypes.fields import GenericRelation,GenericForeignKey
# Create your models here.


class VerifiedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.Verified)

class NotVerifiedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.NotVerified)
    
class RecommendedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Recommendation.Recommended)

class NotRecommendedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Recommendation.NotRecommended)

class Post(models.Model,HitCountMixin):

    class Status(models.TextChoices):
        Verified = 'VD','Verified'
        NotVerified = 'NV','NotVerified'
    
    class Recommendation(models.TextChoices):
        Recommended = 'RCMD','Recommended'
        NotRecommended = 'NCMD','NotRecommended'

    author = models.ForeignKey(User,on_delete=models.CASCADE)
    picture = models.ImageField(null=True,blank=True)       
    title = models.CharField(max_length=300)
    text = models.TextField()
    publish_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.NotVerified)
    recommendation = models.CharField(max_length=4,
                                      choices=Recommendation.choices,
                                      default=Recommendation.NotRecommended)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')    
    objects = models.Manager()
    verified = VerifiedManager()
    notverified = NotVerifiedManager()
    recommended = RecommendedManager()
    notrecommended = NotRecommendedManager()

    class Meta:
        ordering = ['-publish_time']

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_time']
    
    def __str__(self):
        return self.text