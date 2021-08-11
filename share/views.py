from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse

from .models import *
from .forms import FileForm

import os
# Create your views here.
#
# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

def index(request):
    if request.method == "POST":
        if request.POST.get('submit') == 'login':
            # your sign in logic goes here
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
                return render(request, "auctions/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "share/login.html")


def files_view(request):

    files = File.objects.filter(uploader=request.user)
    shared_f = Shared.objects.filter(shared_with=request.user)
    print(shared_f)
    print(shared_f.fi)
    # for f in shared_files:
    #     print(f.file_name)

    return render(request, "share/files.html", {
        'files': files,
    })

def share(request, filename):
    if request.method == "POST":
        shared_file = File.objects.get(file_name=filename)

        user = User.objects.get(username=request.POST["username"])
        newShare = Shared(shared_by=request.user, shared_with=user, shared_file=shared_file)
        newShare.save()
    return HttpResponseRedirect(reverse('files'))


def upload(request):
    newFile = File()
    if request.method == 'POST':
            form = FileForm(request.POST, request.FILES)

            if form.is_valid():

                newFile = File(file=request.FILES['file'], uploader=request.user,
                               file_name=request.FILES['file'].name.replace(' ', '_'),
                               description=request.POST['description'])

                print(f"here you go fam {newFile.file.name}")
                newFile.save()

                # newFile.file_name = newFile.file.name  # to solve duplicates
                # newFile.save()
                print(f"here you go fam {newFile.file.name}")
                print(newFile.file_name)
                # Redirect to the file list after POST
                return HttpResponseRedirect(reverse('files'))
    else:
        form = FileForm()  # An empty, unbound form

    return render(request, 'share/upload.html',
        {'file': newFile,
         'form': form
         }
                  )


def download(request, filename):
    getFile = File.objects.get(file_name=filename)

    if getFile is not None:
        return FileResponse(open(getFile.file.name, 'rb'))
    return HttpResponseRedirect("someerrorpage.html") # create error page