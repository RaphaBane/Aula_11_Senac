from django.contrib import admin
from app.models import Person
from app.models import Book

# Register your models here.
admin.site.register(Person)
admin.site.register(Book)