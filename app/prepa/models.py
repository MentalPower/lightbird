from django.db import models

# Create your models here.
class Town(models.Model):
    name = models.CharField(max_length=200)
    add_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=200)
    town = models.ForeignKey(Town, on_delete=models.PROTECT)
    add_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s (%s)" % (self.town, self.name)

class Status(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_en = models.CharField(max_length=200)
    add_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.name_en)

class Event(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    add_date = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s:%s" % (self.area, unicode(self.add_date))

class Action(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    add_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%s-%s-%s" % (self.event, self.status, self.add_date)

class Scan(models.Model):
    add_date = models.DateTimeField(auto_now_add=True)
    num_towns = models.IntegerField()
    num_breakdowns = models.IntegerField()
    def __unicode__(self):
        return "%d towns and %d breakdowns scanned on %s" % (num_towns, num_breakdowns, add_date)
