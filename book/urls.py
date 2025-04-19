
from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),  # Страница книги (обложка, автор)
    path('book/<int:book_id>/page/<int:page_number>/', views.book_page, name='book_page'),  # Страница с контентом книги
]
