from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import FileForm

import os
# Create your views here.
#
# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))


def loginRedirect(request): # if the user is logged in, redirect to files
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('files'))
    else:
        return HttpResponseRedirect(reverse('login'))


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == "POST":
        print("LGO")

        if request.POST.get('submit') == 'login':

            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(request, username=username, password=password)
            print(user)
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
    else:
        return render(request, "share/login.html")


def view(request, filename):
    file = File.objects.get(file_name=filename)
    comments = Comment.objects.filter(file=file)
    comment_allowed = Shared.objects.filter(shared_file=file).filter(shared_with=request.user).first()
    comment_allowed = True if comment_allowed is not None and comment_allowed.comment_allowed else False

    print(comment_allowed)
    return render(request, 'share/view.html', {
        'file': file,
        'comments': comments,
        'comment_allowed': comment_allowed

    })

@login_required
def files_view(request):
    files = File.objects.filter(uploader=request.user)

    shared_f = Shared.objects.filter(shared_with=request.user)
    l = {}
    for s in shared_f:
        l[File.objects.get(pk=s.shared_file.pk)] = s.comment_allowed

    return render(request, "share/files.html", {
        'files': files,
       'shared_with_me': l
    })

def share(request, filename):
    if request.method == "POST":
        shared_file = File.objects.get(file_name=filename)
        can_comment = True if request.POST.get("canComment", False) == 'on' else False
        user = User.objects.get(username=request.POST["username"])
        newShare = Shared(shared_by=request.user, shared_with=user, shared_file=shared_file, comment_allowed=can_comment)
        newShare.save()
    return HttpResponseRedirect(reverse('files'))

@login_required
def upload(request):
    newFile = File()
    if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)

            if form.is_valid():
                newFile = File(file=request.FILES['file'], uploader=request.user,
                               file_name=request.FILES['file'].name.replace(' ', '_'),
                               description=request.POST['description'])

                newFile.save()

                flname = os.path.basename(newFile.file.name)
                newFile.file_name = flname  # update the name with the new unique name
                newFile.save()

                # Redirect to the file list after POST
                return HttpResponseRedirect(reverse('files'))
    else:
        form = FileForm()

    return render(request, 'share/upload.html',{
        'file': newFile,
         'form': form
         })


def download(request, filename):
    files = File.objects.all()
    for f in files:
        print(f)
    print(filename)
    getFile = File.objects.get(file_name=filename)

    if getFile is not None:
        return FileResponse(open(getFile.file.name, 'rb'))
    return HttpResponseRedirect("someerrorpage.html") # create error page


def comment(request, pk):
    if request.method == 'POST':
        grab_file = File.objects.get(pk=pk)
        newComment = Comment(user=request.user, file=grab_file, comment=request.POST['comment'])
        print(newComment)
        newComment.save()

    return HttpResponseRedirect(reverse('view', kwargs={'filename': grab_file.file_name}))
