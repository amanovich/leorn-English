import json

from django.contrib.admin import display
from django.http import HttpResponse
from django.contrib import admin
from .models import Book, Page, Question
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO


@admin.action(description="Экспортировать книгу с её страницами и вопросами в JSON")
def export_full_book_json(modeladmin, request, queryset):
    data = []

    for book in queryset:
        book_data = {
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'cover_image': book.cover_image.url if book.cover_image else None,
            'pages': []
        }

        for page in book.pages.all():
            page_data = {
                'number': page.number,

                'text': page.text,
                'audio': page.audio.url if page.audio else None,
                'audio_label': page.audio_label,
                'questions': []
            }

            for question in page.questions.all():
                page_data['questions'].append({
                    'question_text': question.question_text,
                    'correct_answer': question.correct_answer
                })

            book_data['pages'].append(page_data)

        data.append(book_data)

    response = HttpResponse(
        json.dumps(data, indent=4, ensure_ascii=False),
        content_type="application/json"
    )
    response['Content-Disposition'] = 'attachment; filename=full_books_export.json'
    return response

@admin.action(description="Экспортировать книгу в PDF")
def export_book_to_pdf(modeladmin, request, queryset):
    if queryset.count() != 1:
        return HttpResponse("Пожалуйста, выбери только одну книгу для экспорта в PDF.")

    book = queryset.first()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, f"Книга: {book.title}")
    y -= 25
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Автор: {book.author}")
    y -= 25
    p.drawString(50, y, f"Описание: {book.description[:200]}...")
    y -= 40

    for page in book.pages.all():
        if y < 150:
            p.showPage()
            y = height - 50

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, f"Страница {page.number} (метка: {page.label})")
        y -= 20
        p.setFont("Helvetica", 12)
        text = page.text[:300].replace('\n', ' ')
        p.drawString(50, y, f"Текст: {text}...")
        y -= 20

        if page.questions.exists():
            p.setFont("Helvetica-Oblique", 11)
            for q in page.questions.all():
                if y < 100:
                    p.showPage()
                    y = height - 50
                p.drawString(60, y, f"Вопрос: {q.question_text}")
                y -= 15
                p.drawString(60, y, f"Ответ: {q.correct_answer}")
                y -= 20

        y -= 20

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    actions = [export_full_book_json, export_book_to_pdf]
    search_fields = ('title', 'author')
    list_filter = ('author',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class PageAdmin(admin.ModelAdmin):
    list_display = ('book', 'number')
    list_display = ('book', 'number', 'audio_label')

    inlines = [QuestionInline]
    search_fields = ('book__title', 'number')
    list_filter = ('book',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'page')
    search_fields = ('question_text', 'correct_answer', 'page__book__title')
    list_filter = ('page__book',)


admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)

