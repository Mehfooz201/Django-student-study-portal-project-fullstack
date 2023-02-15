from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('notes_detail/<int:pk>', views.details_note, name='notes-details'),

    path('homework/', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),

    path('youtube/', views.youtube, name='youtube'),

    path('todo/', views.todo, name='todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),

    path('books/', views.books, name='books'),

    path('profile/', views.profile, name='profile'),

    path('dictionary/', views.dictionary, name='dictionary'),

    path('wikipedia/', views.wiki, name='wiki'),

    path('conversion/', views.conversion, name='conversion'),

    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),

    path('logout/', views.user_logout, name='logout'),

]