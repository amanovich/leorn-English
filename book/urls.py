from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookviewSet
from . import views
from .views import BookviewSet, PageViewSet
from django.contrib.auth.views import LoginView
from .forms import TeacherLoginForm
from .views import teacher_books

router = DefaultRouter()
router.register(r'api/books', BookviewSet, basename='book')
router.register(r'api/pages', PageViewSet, basename='page')

urlpatterns = [
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/page/<int:page_number>/', views.book_page, name='book_page'),
    path('', include(router.urls)),
    # path('login/', loginView.as_view(authentication_from=teacherloginFrom), name='login'),
    path('teacher-books/', teacher_books, name='teacher_books'),

]
