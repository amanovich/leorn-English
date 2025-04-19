from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Page

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
    book = Book.objects.get(id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})