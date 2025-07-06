from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from app.views import ServerInfoView, HelloWorldView, WelcomeView, PeopleView, BookListJsonView, BookListView, BookCreateView, BookGetView, BookUpdateView, BookDeleteView, contact_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', HelloWorldView.as_view(), name='hello'),
    path('server-info/', ServerInfoView.as_view(), name='server_info'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('people/', PeopleView.as_view(), name='people'),
    path('book/json/', BookListJsonView.as_view(), name='book_list_json'),
    path('book/list', BookListView.as_view(), name='book_list'),
    path('book/<int:book_id>', BookGetView.as_view(), name='book_get'),
    path('book/', BookCreateView.as_view(), name='book_create'),
    path('book/edit/<int:book_id>', BookUpdateView.as_view(), name='book_update'),
    path('book/delete/<int:book_id>', BookDeleteView.as_view(), name='book_delete'),
    path('contact/', contact_view, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)