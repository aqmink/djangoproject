from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.db.models.query import QuerySet
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render 
from django.urls import reverse_lazy
from django.views.generic import ( 
    CreateView, 
    DeleteView, 
    DetailView,
    ListView,
    UpdateView,
)

from .models import Book, Author, Comment
from .forms import CommentCreationForm, RegistrationForm, LoginForm


def home_page(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, 'bookshelf/home.html')
    else:
        return redirect('registration')


class AuthorList(ListView):
    model = Author
    template_name = 'bookshelf/authors.html'
    context_object_name = 'author_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Author.objects.all()


class AuthorDetail(DetailView):
    model = Author
    context_object_name = 'author'
    slug_url_kwarg = 'author_slug'
    template_name = 'bookshelf/author-detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.filter(author__slug=self.kwargs['author_slug'])
        return context


class BookList(ListView):
    model = Book
    template_name = 'bookshelf/books.html'
    context_object_name = 'book_list'

    def get_queryset(self) -> QuerySet[Any]:
        return Book.objects.all().order_by('title').select_related('author')


class BookDetail(DetailView):
    model = Book
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'
    template_name = 'bookshelf/book-detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(book__slug=self.kwargs['book_slug']).select_related('name')
        return context


class CommentCreate(CreateView):
    form_class = CommentCreationForm
    template_name = 'bookshelf/create.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        initial = {'book': Book.objects.get(slug=kwargs['book_slug'])}
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form, 'book': initial['book']})

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_detail', self.kwargs['book_slug'])
        return render(request, self.template_name, {'form': form})


class CommentDelete(DeleteView):
    model = Comment
    template_name = 'bookshelf/delete.html'
    success_url = reverse_lazy('books')


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentCreationForm
    template_name = 'bookshelf/update.html'


class Registration(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'bookshelf/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        login(self.request, user=user)
        return redirect('home')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'bookshelf/login.html'

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class SearchView(ListView):
    model = Book
    template_name = 'bookshelf/search_results.html'

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('form_input')
        if query:
            result = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query)).select_related('author')
            return result
