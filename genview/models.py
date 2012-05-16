import registration

__author__ = 'jaume'
import datetime
from snag.registration import models
from django.db import models
from django.contrib.auth.models import User


try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

class Creature(models.Model):
    creation_date = models.DateField(default=datetime.date.today)
    def __unicode__(self):
        return 'Ccreature: %s' % self.creation_date

class Generation(models.Model):
    number = models.PositiveIntegerField(default="0")
    creature_id = models.ForeignKey(Creature)
    def __unicode__(self):
        return 'Generation: %s' % (self.number, self.creation_id)

class Chromosome(models.Model):
    data = models.TextField(max_length=2000)
    generation_id = models.ForeignKey(Generation)
    def __unicode__(self):
        return 'Chromosomes: %s | $s' % (self.data, self.generation_id)

class Gens(models.Model):
    name = models.TextField(max_length=2000)
    def __unicode__(self):
        return 'Gens: %s' % self.name

class Contents(models.Model):
    question = models.TextField(max_length=2000)
    answer = models.TextField(max_length=2000)
    gen_id = models.ForeignKey(Gens)
    def __unicode__(self):
        return 'Contents: %s | %s | %s' % (self.question, self.answer, self.gen_id)

class Tasks(models.Model):

    user_id =models.OneToOneField(User)
    chromosome_id = models.ForeignKey(Chromosome)
    test_date = models.DateField(default=datetime.date.today)
    total_test_time = models.IntegerField()
    contents_id = models.ForeignKey(Contents)
    test_ok = models.BooleanField()
    def __unicode__(self):
        return 'Contents: %s | %s | %s' % (self.question, self.answer, self.gen_id)



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