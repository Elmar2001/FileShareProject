from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import os


class File(models.Model):
    file = models.FileField(upload_to='Files')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=128)
    description = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(os.path.basename(self.file.name))


class Shared(models.Model):
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_by")
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_with")
    shared_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="shared_file")
    comment_allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.shared_by.username + ' shared ' + self.shared_file.file_name + ' with ' + self.shared_with.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor")
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="commented_file")
    comment = models.TextField(max_length=256)

    def __str__(self):
        return self.user.username + " commented " + self.comment + " on " + self.file.file_name
