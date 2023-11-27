from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('books', views.BookList.as_view(), name="books"),
    path('authors', views.AuthorList.as_view(), name="authors"),
    path('registration', views.Registration.as_view(), name="registration"),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('search_results', views.SearchView.as_view(), name='search_results'),
    path('books/<book_slug>', views.BookDetail.as_view(), name="book_detail"),
    path('authors/<author_slug>', views.AuthorDetail.as_view(), name="author_detail"),
    path('books/<book_slug>/create', views.CommentCreate.as_view(), name="create"),
    path('books/<book_slug>/<int:pk>/update', views.CommentUpdate.as_view(), name="update"),
    path('books/<book_slug>/<int:pk>/delete', views.CommentDelete.as_view(), name="delete"),
]
