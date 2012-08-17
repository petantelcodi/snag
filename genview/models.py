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
    current_generation = models.IntegerField(default="0")
    def __unicode__(self):
        return '%s' % self.id

class Chromosome(models.Model):
    data = models.TextField(max_length=2000)
    creature_id = models.ForeignKey(Creature)
    generation = models.PositiveIntegerField(default="0")
    user_id =models.ForeignKey(User, default = 0)
    def __unicode__(self):
        return 'Chromosomes: %s, generation: %s' % (self.data, self.generation_id)

class Tasks(models.Model):
    user_id =models.ForeignKey(User)
    chromosome_id = models.ForeignKey(Chromosome)
    test_date = models.DateField(default=datetime.date.today)
    total_test_time = models.IntegerField()
    test_ok = models.IntegerField()
    def __unicode__(self):
        return 'Contents: %s | %s | %s' % (self.question, self.answer, self.gen_id)

'''
class Generation(models.Model):
    number = models.PositiveIntegerField(default="0")
    creature_id = models.ForeignKey(Creature)
    def __unicode__(self):
        return 'Generation: %s, Creation %s' % (self.number, self.creation_id)
'''

'''
class Gens(models.Model):
    name = models.TextField(max_length=2000)
    def __unicode__(self):
        return 'Gens: %s' % self.name
'''


class Contents(models.Model):
    question = models.TextField(max_length=2000)
    answer = models.TextField(max_length=2000)
    #gen_id = models.ForeignKey(Gens)
    def __unicode__(self):
        return 'Contents: %s | %s | %s' % (self.question, self.answer, self.gen_id)


