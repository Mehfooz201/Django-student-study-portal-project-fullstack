from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Note, Homework, Todo
from .forms import NoteForm, HomeworkForm, DashboardForm, TodoForm, ConversionForm, ConversionLengthForm, ConversionMassForm, UserRegistrationForm
from youtubesearchpython import VideosSearch 
import requests
import wikipedia
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    notes = Note.objects.filter(user=request.user)
    if request.method=='POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            c = Note(user=request.user, title=title, description=description)
            c.save()
            messages.success(request, f'''Notes added from '{request.user}' successfully!''')
    else:    
        form = NoteForm()
    context = {
        'notes':notes, 'form' : form}
    return render(request, 'dashboard/notes.html', context)

@login_required
def delete_note(request, pk=None):
    Note.objects.get(id=pk).delete()
    return redirect('notes')

@login_required
def details_note(request, pk):
    notes = Note.objects.get(id=pk)
    return render(request, 'dashboard/notes_detail.html', {'notes':notes})


@login_required
def homework(request):
    if request.method=='POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            subject = form.cleaned_data['subject']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            due = form.cleaned_data['due']
            is_finished = form.cleaned_data['is_finished']
            s = Homework(user=request.user, subject=subject, title=title, description=description, due=due, is_finished=is_finished )
            s.save()
            messages.success(request, f'''Homework added from '{request.user}' successfully!''')
            form = HomeworkForm()
    else:
        form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks':homeworks, 'homework_done':homework_done, "form":form}
    return render(request, 'dashboard/homework.html',context)


def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')



#YouTube
@login_required
def youtube(request):
    if request.method=='POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10) 
        result_list = []
        for i in video.result()['result']:
            result_dic = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dic['description']=desc
            result_list.append(result_dic)
            context = {
                'form':form,
                'results': result_list
                }

        return render(request, 'dashboard/youtube.html', context)
    else:   
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/youtube.html', context)


#Todo
@login_required
def todo(request):
    if request.method=='POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False

            title = form.cleaned_data['title']
            is_finished = form.cleaned_data['is_finished']
            todos = Todo(user=request.user, title=title, is_finished=is_finished )
            todos.save()
            messages.success(request, f'''Todo added from '{request.user}' successfully!''')
            form = TodoForm()
    else:
        form = TodoForm()

    todos = Todo.objects.filter(user=request.user)
    if len(todos) == 0:
            todos_done = True
    else:
        todos_done = False
    context =  {'todos':todos, "form":form, 'todos_done':todos_done}
    return render(request, 'dashboard/todo.html', context)

def delete_todo(request, pk):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def update_todo(request, pk):
    todos = Todo.objects.get(id=pk)
    if todos.is_finished == True:
        todos.is_finished = False
    else:
        todos.is_finished = True
    todos.save()
    return redirect('todo')


#Profile
@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)

    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    
    context = {
        'homeworks' :homeworks, 
        'todos' : todos,
        'homework_done' : homework_done,
        'todos_done': todos_done
    }
    return render(request, 'dashboard/profile.html', context)


#Books
@login_required
def books(request):
    if request.method=='POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dic = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dic)
            context = {
                'form':form,
                'results': result_list
                }

        return render(request, 'dashboard/books.html', context)
    else:   
        form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/books.html', context)



#Dictionary
@login_required
def dictionary(request):
    if request.method=='POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input' : text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example' : example,
                'synonyms':synonyms  }
        except:
            context = {'form': form, 'input' : '' }
        return render(request, 'dashboard/dictionary.html', context)

    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request, 'dashboard/dictionary.html', context)



#wikipedia
@login_required
def wiki(request):
    if request.method=='POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        try:
            context = {
                'form' : form,
                'title' : search.title,
                'link' : search.url,
                'details' : search.summary
                }
        except:
            context = {
                'form' : form,
                'title' : '',
            }
        return render(request, 'dashboard/wiki.html', context)

    else:
        form = DashboardForm()
    context = {'form' : form}
    return render(request, 'dashboard/wiki.html', context)


#Profile
@login_required
def conversion(request):
    if request.method=='POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] =='length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form': measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0 :
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form': measurement_form,
                    'input':True,
                    'answer' : answer
                }

        if request.POST['measurement'] =='mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form': measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0 :
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form': measurement_form,
                    'input':True,
                    'answer' : answer
                }
    else:
        form = ConversionForm()
        context = {'form':form, 'input':False}
    return render(request, 'dashboard/conversion.html',context)



#Register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'''Account has been created for '{username}', successfully!''')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
            'form':form
        }
    return render(request, 'dashboard/register.html',context)


def user_logout(request):
    logout(request)
    return redirect('login')
