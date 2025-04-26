from rest_framework import serializers
from .models import Book, Page, Question




class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'correct_answer']


class PageSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['id', 'number', 'text', 'audio', 'audio_label', 'questions']


class BookSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)  # 👈 добавлено, чтобы Book включал Page

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'pages']




