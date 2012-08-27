from django.db import models

class Scan(models.Model):
    num_towns = models.IntegerField(default=-1)
    num_breakdowns = models.IntegerField(default=-1)
    time_taken = models.FloatField(default=0)
    record_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return "%d towns and %d breakdowns scanned on %s" % (self.num_towns, self.num_breakdowns, self.record_time)

class Town(models.Model):
    name = models.CharField(max_length=200)
    scan_added = models.ForeignKey(Scan, on_delete=models.PROTECT)
    def __unicode__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=200)
    town = models.ForeignKey(Town, on_delete=models.PROTECT)
    scan_added = models.ForeignKey(Scan, on_delete=models.PROTECT)
    def __unicode__(self):
        return "%s (%s)" % (self.town, self.name)

class Status(models.Model):
    name = models.CharField(max_length=200, unique=True)
    name_en = models.CharField(max_length=200)
    scan_added = models.ForeignKey(Scan, on_delete=models.PROTECT)
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.name_en)

class Event(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    scan_added = models.ForeignKey(Scan, on_delete=models.PROTECT, related_name='added')
    scan_last_seen = models.ForeignKey(Scan, on_delete=models.PROTECT, related_name='last_seen')
    def __unicode__(self):
        return "%s:%s:%s" % (self.area, self.scan_added, self.scan_last_seen)

class Action(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    scan_added = models.ForeignKey(Scan, on_delete=models.PROTECT)
    def __unicode__(self):
        return "%s-%s-%s" % (self.event, self.status, self.add_date)
