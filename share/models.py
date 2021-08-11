from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class File(models.Model):
    file = models.FileField(upload_to='Files')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=128)
    description = models.TextField()
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.file_name

    # def get_absolute_url(self):
    #     return reverse()


class Shared(models.Model):
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_by")
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_with")
    shared_file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="shared_file")

    def __str__(self):
        return self.shared_by.username + ' shared ' + self.shared_file.file_name + ' with ' + self.shared_with.username

