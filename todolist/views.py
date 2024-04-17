from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/todoview.html', {'form': form, 'todo': todo})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
            # todo = get_object_or_404(Todo, pk=todo_pk)
            # return render(request, 'todo/todoview.html', {'form': form, 'message': 'Sucsse updating'})
        except ValueError:
            return render(request, 'todo/todoview.html', {'form': form, 'message': 'Error apdating'})


def createtodo(request):
    # return render(request, 'todo/todo.html')
    if request.method == 'GET':
        return render(request, 'todo/todo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/todo.html', {'form': TodoForm(), 'error': 'Error ccured'})


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm})
    else:
        # create new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form': UserCreationForm, 'error': 'that user name already taken'})

        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm, 'error': 'password did not matcing'})


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/current.html', {'toso_list': todos})


def userlogut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/logn.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/logn.html', {'form': AuthenticationForm, 'error': 'User Name or password Not correct'})
        else:
            login(request, user)
            return redirect('currenttodos')
