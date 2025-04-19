import json
from django.http import HttpResponse
from django.contrib import admin
from .models import Book, Page, Question


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


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    actions = [export_full_book_json]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class PageAdmin(admin.ModelAdmin):
    list_display = ('book', 'number')
    inlines = [QuestionInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Page, PageAdmin)

