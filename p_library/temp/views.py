from django.shortcuts import render, redirect
#from p_library.models import Book, Author, PublishingHouse
from django.http import HttpResponse
from django.template import loader
#from p_library.forms import AuthorForm, BookForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect

# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    index_data = {
        "title": 'Главная страница',
    }
    return HttpResponse(template.render(index_data,request))


def books_list(request):
    books=Book.objects.all()
    book_names=[]
    for book in books:
        book_names.append(book.title)
    return HttpResponse(book_names)

def index(request):
    template=loader.get_template('index.html')
    books = Book.objects.all()
    biblio_data={
        "title": "мою библиотеку",
        "books": books,
    }
    return HttpResponse(template.render(biblio_data, request))

def books(request):
    template = loader.get_template('book_list.html')
    books = Book.objects.all()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
           }
    return HttpResponse(template.render(biblio_data, request))


def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/books/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/books/')
            book.copy_count += 1
            book.save()
        return redirect('/books/')
    else:
        return redirect('/books/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/books/')
        else:
            book = Book.objects.filter(id=book_id).first()
        if not book:
            return redirect('/books/')
        if book.copy_count < 1:
            book.copy_count = 0
        else:
            book.copy_count -= 1
        book.save()
        return redirect('/books/')
    else:
        return redirect('/books/')


def publishers(request):
    template = loader.get_template('publishers.html')
    publishers = PublishingHouse.objects.all().order_by('company_name')
    books_by_publisher = {}
    for publish_comp in publishers:
        books_by_publisher[publish_comp.company_name] = Book.objects.filter(publisher=publish_comp).order_by('title')

    publisher_books_data = {
            "title": "СПИСОК КНИГ ПО ИЗДАТЕЛЬСТВАМ",
            "books": books_by_publisher,
        }
    return HttpResponse(template.render(publisher_books_data, request))

class AuthorEdit(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('author_list')
    template_name = 'author_edit.html'

class AuthorList(ListView):
    model = Author
    template_name = 'authors_list.html'

def author_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    if request.method=='POST':
        author_formset=AuthorFormSet(request.POST, request.FILES, prefix='authors')
        if author_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            return HttpResponseRedirect(reverse_lazy('author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
    return render(request, 'manage_authors.html', {'author_formset':author_formset})

def books_authors_create_many(request):
    AuthorFormSet = formset_factory(AuthorForm, extra=2)
    BookFormSet = formset_factory(BookForm, extra=2)
    if request.method == 'POST':
        author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
        book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
        if author_formset.is_valid() and book_formset.is_valid():
            for author_form in author_formset:
                author_form.save()
            for book_form in book_formset:
                book_form.save()
            return HttpResponseRedirect(reverse_lazy('author_list'))
    else:
        author_formset = AuthorFormSet(prefix='authors')
        book_formset = BookFormSet(prefix='books')
    return render(
        request,
        'manage_books_authors.html',
        {
            'author_formset': author_formset,
            'book_formset':book_formset,
        }
    )