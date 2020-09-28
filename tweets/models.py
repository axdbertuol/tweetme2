import random
from django.db import models

class Tweet(models.Model):
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f'{self.content}'

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 1000)
        }