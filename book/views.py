from django.shortcuts import render, get_object_or_404
from .models import Book, Page
from rest_framework import viewsets
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PageSerializer
from .serializers import QuestionSerializer
from .models import Question
from rest_framework.pagination import PageNumberPagination
from .decorators import teacher_required

@teacher_required
def add_book(request):
    # логика добавления книги
    return render(request, 'add_book.html')

@teacher_required
def teacher_books(request):
    books = Book.objects.filter(target_role='teacher')
    return render(request, 'teacher_books.html', {'books': books})



def book_cover(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/cover.html', {'book': book})


def book_page(request, book_id, page_number):
    page = get_object_or_404(Page, book_id=book_id, number=page_number)
    questions = page.questions.all()
    result = None

    if request.method == 'POST':
        correct = 0
        for q in questions:
            answer = request.POST.get(f'question_{q.id}', '').strip().lower()
            if answer == q.correct_answer.lower():
                correct += 1
        result = f"{correct} out of {questions.count()} correct"

    return render(request, 'book/page.html', {
        'page': page,
        'questions': questions,
        'result': result,
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})

class BookviewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fieldsn = ['title', 'author']
    pagination_class = PageNumberPagination


class PageViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Page.objects.all()
        serializer_class = PageSerializer
        filter_backends = [DjangoFilterBackend]
        filterset_fields = ['id', 'book']
        pagination_class = PageNumberPagination


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['page', 'question_text']
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination