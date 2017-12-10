from django.contrib.auth.models import User
from django.db import models


class DirectoryInfo(models.Model):
    """Store specific LDAP user information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="directory_info")
    source = models.CharField(max_length=100)

    def __str__(self):
        return "{user} stored into {source}".format(user=self.user.username, source=self.source)
