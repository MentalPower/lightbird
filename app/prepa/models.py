from django.db import models

# Create your models here.
class Town(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    add_date = models.DateTimeField('date added')
    def __unicode__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=200)
    town = models.ForeignKey(Town, on_delete=models.PROTECT)
    add_date = models.DateTimeField('date added')
    def __unicode__(self):
        return self.town

class Event(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    add_date = models.DateTimeField('date detected')
    def __unicode__(self):
        return "%s:%s" % (self.area, unicode(self.add_date))

class Status(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_en = models.CharField(max_length=200, unique=True)
    add_date = models.DateTimeField('date added')
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.name_en)

class Action(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    add_date = models.DateTimeField('date detected')
    def __unicode__(self):
        return "%s-%s-%s" % (self.event, self.status, self.add_date)
