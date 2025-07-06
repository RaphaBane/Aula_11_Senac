import json
import os
import platform
import smtplib
import socket
from datetime import datetime

import cloudinary
import cloudinary.uploader
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from app.models import Person
from app.models import Book
from app.forms import BookForm
from app.forms import ContactForm

# View 1 - Hello World (FBV)
def hello_view(request):
    response = { "message": "Hello, World!" }
    return JsonResponse(response)

# View 1 - Hello World (CBV)
class BaseHelloView(View):
    base_message = "Hello, World from CBV!"

    def get(self, request):
        return JsonResponse({
            'message': f'{self.base_message} - {datetime.now()}!'
        })

class HelloWorldView(BaseHelloView):
    base_message = "Hello, World!"

class ServerInfoView(View):
    def get(self, request):
        hostname = socket.gethostname()
        python_version = platform.python_version()
        return JsonResponse({
            'python_version': python_version,
            'hostname': hostname
        })

class WelcomeView(TemplateView):
    template_name = "app/welcome.html" #<project_root>/templates/app/welcome.html

    def get_context_data(self, **kwargs): #sobreescrita
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.GET.get('name', 'Visitante')
        return context

class PeopleView(View):
    def get(self, request):
        people = Person.objects.all() # SELECT * FROM person
        data = [{'name': p.name, 'age': p.age} for p in people]
        return JsonResponse({'people': data})

# ---- x ---- x ---- x ---- x ---- x ---- x ---- x ---- x ---- x ----

class BookListJsonView(View):
    def get(self, request):
        books = Book.objects.all().values
        return JsonResponse(list(books), safe=False)

class BookListView(ListView):
    model = Book
    template_name = "app/book_list.html"
    context_object_name = "books"

class BookGetView(DetailView):
    model = Book
    template_name = "app/book_detail.html"
    context_object_name = "book"
    pk_url_kwarg = "book_id"

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    success_url = reverse_lazy('book_list') # redireciona após o cadastro

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "app/book_form.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Json invalid'}, status=400)

        # Monta os kwargs com os dados e instância
        kwargs = self.get_form_kwargs()
        kwargs['data'] = body
        kwargs['instance'] = self.object

        form = self.get_form(**kwargs)

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class BookDeleteView(DeleteView):
    model = Book
    template_name = "app/book_confirm_delete.html"
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy('book_list')

def contact_view(request):
    form = ContactForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        file = form.cleaned_data.get('attachment')

        filename = f'arquivo_teste'

        upload_result = cloudinary.uploader.upload(
            file=file,
            asset_folder='uploads',
            public_id=filename,
            override=True,
            resource_type="raw"
        )

        smtplib.SMTP.debuglevel = 1

        message_body = message + f'\n\nFaça o download em: {upload_result["secure_url"]}'

        email_message = EmailMessage(
            subject=f'Contato de {name}',
            body=message_body,
            from_email=email,
            to=['aula.raphaelaragaoparreira@gmail.com']
        )

        email_message.send()

        # Simula envio
        context = {'success': True, 'name': name }

        return render(request, 'app/contact.html', context)
    return render(request, 'app/contact.html', {'form': form})