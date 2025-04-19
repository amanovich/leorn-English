from django.db import models

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

    def __str__(self):
        return f"Page {self.number} of {self.book.title}"

class Question(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Q: {self.question_text} (Page {self.page.number})"
