__author__ = 'jaume'

from django.db import models
from treebeard.mp_tree import MP_Node

class Category(MP_Node):
    name = models.CharField(max_length=30)
    name2 = models.CharField(max_length=30)
    namewwww = models.CharField(max_length=30)
    namerrr = models.CharField(max_length=30)

    node_order_by = ['name']

    def __unicode__(self):
        return 'Category: %s' % self.name

"""

#from tinymce import models as tinymce_models

class Participant(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='images/')
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    website = models.URLField()

    def __unicode__(self):
        return '%s %s %s' % (self.id, self.first_name, self.last_name)

    class Meta:
        ordering = ["first_name"]

class Pic(models.Model):
    name = models.CharField(max_length=30)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=50)
    pics = models.ImageField(upload_to='images/')

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        ordering = ["name"]

class Conversation(models.Model):
    title = models.CharField(max_length=60)
    teaser = models.TextField(max_length=210)
    #body = tinymce_models.HTMLField()
    body = models.TextField(max_length=1000)
    audio_file = models.FileField(upload_to='audios/')
    participants = models.ManyToManyField(Participant)
    date = models.DateField()
    pic = models.ManyToManyField(Pic)
    def __unicode__(self):
        return u'%s - Title: %s | Date: %s ' % (self.id, self.title, self.date)

    class Meta:
        ordering = ["date"]

class Page(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField(max_length=1000)

    def __unicode__(self):
        return u'<h2>%s</h2><p>%s</p>' % (self.title, self.body)

    class Meta:
        ordering = ["title"]


"""