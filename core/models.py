from django.db import models


class Logging(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    command = models.TextField()


class Admin(models.Model):
    tg_id = models.IntegerField(primary_key=True)
