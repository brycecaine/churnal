from __future__ import unicode_literals

from django.db import models

class GoogleUser(models.Model):
    client_id = models.CharField(max_length=300)
    journal_entries_path = models.CharField(max_length=1000)
