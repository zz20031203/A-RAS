from django.db import models

class UploadedImage(models.Model):
    openid = models.CharField(max_length=255)  # 存储openid
    image = models.ImageField(upload_to='images/')  # 存储图片

    def __str__(self):
        return f"Image uploaded by {self.openid}"
