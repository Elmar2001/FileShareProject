from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import FileForm

import os


def login_redirect(request):  # if the user is logged in, redirect to files
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('files'))
    return HttpResponseRedirect(reverse('login'))


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'login':

            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("files"))  # redirect to files
            else:
                return render(request, "share/login.html", {
                    "message": "Invalid username and/or password."
                })
        elif request.POST.get('submit') == 'register':
            username = request.POST["username"]
            email = request.POST["email"]

            # Ensure password matches confirmation
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]

            if password1 != password2:
                return render(request, "share/login.html", {
                    "message": "Passwords must match."
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
            except IntegrityError:
                return render(request, "share/login.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            print("logging in")
            return HttpResponseRedirect(reverse("index"))

    return render(request, "share/login.html")


def view(request, filename):
    try:
        file = File.objects.get(file_name=filename)
    except File.DoesNotExist:
        return HttpResponse('Exception: File Not Found')

    comments = Comment.objects.filter(file=file)
    comment_allowed = Shared.objects.filter(shared_file=file).filter(shared_with=request.user).first()
    comment_allowed = True if comment_allowed is not None and comment_allowed.comment_allowed else False

    return render(request, 'share/view.html', {
        'file': file,
        'comments': comments,
        'comment_allowed': comment_allowed
    })


@login_required
def files_view(request):
    files = File.objects.filter(uploader=request.user)

    shared_ = Shared.objects.filter(shared_with=request.user)

    shared_files = []

    for s in shared_:
        shared_files.append(File.objects.get(pk=s.shared_file.pk))

    return render(request, "share/files.html", {
        'files': files,
        'shared_with_me': shared_files
    })


def share(request, filename):
    if request.method == "POST":
        shared_file = File.objects.get(file_name=filename)
        can_comment = True if request.POST.get("canComment", False) == 'on' else False
        try:
            user = User.objects.get(username=request.POST["username"])
        except User.DoesNotExist:
            return HttpResponse("The user does not exist")
        new_share = Shared(shared_by=request.user, shared_with=user, shared_file=shared_file, comment_allowed=can_comment)
        new_share.save()
    return HttpResponseRedirect(reverse('files'))


@login_required
def upload(request):
    new_file = File()
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            new_file = File(file=request.FILES['file'], uploader=request.user,
                            file_name=request.FILES['file'].name,
                            description=request.POST['description'])

            new_file.save()

            fname_unique = os.path.basename(new_file.file.name)
            new_file.file_name = fname_unique  # update the name with the new unique name
            new_file.save()

            # Redirect to the file list after POST
            return HttpResponseRedirect(reverse('files'))
    else:
        form = FileForm()

    return render(request, 'share/upload.html', {
         'file': new_file,
         'form': form
         })


@login_required
def download(request, filename):
    try:
        get_file = File.objects.get(file_name=filename)
    except File.DoesNotExist:
        return HttpResponse('Exception: File Not Found')

    if get_file is not None:
        return FileResponse(open(get_file.file.name, 'rb'))
    return HttpResponseRedirect("404.html") # create error page


def comment(request, pk):
    if request.method == 'POST':
        get_file = File.objects.get(pk=pk)
        new_comment = Comment(user=request.user, file=get_file, comment=request.POST['comment'])
        new_comment.save()

    return HttpResponseRedirect(reverse('view', kwargs={'filename': get_file.file_name}))

