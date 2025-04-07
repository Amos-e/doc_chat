from django.db import models


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return "%s --> %s" % (self.name, self.contact)
    

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    msg = models.TextField()
    bearer = models.CharField(max_length=255)

    def __str__(self):
        return "%s -->%s"%(self.bearer, self.msg)
