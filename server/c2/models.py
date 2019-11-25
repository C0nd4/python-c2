from django.db import models


class command(models.Model):
    process = models.CharField(max_length=20)
    arguments = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.process + " " + self.arguments

class client(models.Model):
    uuid = models.CharField(max_length=36)
    ip = models.CharField(max_length=15)
    hostname = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    commands = models.ManyToManyField(command)

    def __str__(self):
        return self.uuid
