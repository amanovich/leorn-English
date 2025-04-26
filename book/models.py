from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'учитель'),
        ('student', 'студент'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_teacher(self):
        return self.role =='teacher'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.title

class Page(models.Model):
    book = models.ForeignKey(Book, related_name='pages', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    text = models.TextField()
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    audio_label = models.CharField(max_length=255, blank=True)


    # def save(self, *args, **kwargs):
    #     self.label = f"{self.book.id}.{self.number}"
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.book_id and self.number:
            self.audio_label = f"{self.book.id}.{self.number}"
        super().save(*args, **kwargs)



    def __str__(self):
        return f"Page {self.number} of {self.book.title}"


class Question(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Page {self.page.number} - {self.page.label or 'no label'}"
