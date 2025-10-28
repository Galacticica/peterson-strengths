from django.db import models

class Review(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return f"{self.author} - {self.rating}/5"
