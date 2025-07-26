from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Note
from django.http import HttpResponseForbidden
from rest_framework import generics, permissions
from .serializers import NoteSerializer

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

def user_login(requests):
    if requests.method == 'POST':
        form = AuthenticationForm(data=requests.POST)
        if form.is_valid():
            user = form.get_user()
            login(requests, user)
            return redirect('home')

    else:
        form = AuthenticationForm()
    return render(requests, 'account/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    notes = request.user.notes.all().order_by('-updated_at')
    return render(request, 'pages/home.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title:
            Note.objects.create(user=request.user, title=title, content=content)
            return redirect('home')
    return render(request, 'pages/note_form.html', {'action': 'Create'})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return redirect('home')
    return render(request, 'pages/note_form.html', {'note': note, 'action': 'Edit'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        note.delete()
        return redirect('home')
    return render(request, 'pages/note_delete_confirm.html', {'note': note})


# API
class NoteListCreateAPI(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NoteRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)