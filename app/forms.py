from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta: # classe interna para configuração do formulário
        model = Book # qual o model será utilizado como base
        fields = ['title', 'author', 'pages', 'published_date'] # quais campos do model serão expostos no formulário
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'author' : forms.TextInput(attrs={'class' : 'form-control'}),
            'pages' : forms.NumberInput(attrs={'class' : 'form-control', 'min': '10'}),
            'published_date' : forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        help_texts = {
            'pages': 'Informe um número inteiro maior que 10.',
            'published_date': 'Use o formato YYYY-MM-DD.'
        }
        labels = {
            'title' : 'Título do Livro',
            'author' : 'Autor do Livro',
            'pages' : 'Número de páginas',
            'published_date' : 'Data de Publicação',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['published_date'].input_formats = ['%Y-%m-%d']

class ContactForm(forms.Form):
    name = forms.CharField(label="Seu nome", max_length=100)
    email = forms.EmailField(label="E-mail")
    message = forms.CharField(label="Mensagem", widget=forms.Textarea)
    attachment = forms.FileField(label="Anexo", required=False)

