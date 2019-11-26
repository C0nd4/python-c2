from django.db import models
import django_tables2 as tables

class command(models.Model):
    process = models.CharField(max_length=20)
    arguments = models.CharField(max_length=1000, blank=True)
    
    def __str__(self):
        return self.process + " " + self.arguments

class client(models.Model):
    uuid = models.CharField(max_length=36)
    ip = models.CharField(max_length=15)
    hostname = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    commands = models.ManyToManyField(command)
    lastBeacon = models.IntegerField(default=0)
    maxFails = models.IntegerField(default=10)
    lowTime = models.IntegerField(default=1)
    highTime = models.IntegerField(default=10)

    def __str__(self):
        return self.uuid
class ClientTable(tables.Table):
    class Meta:
        model = client
