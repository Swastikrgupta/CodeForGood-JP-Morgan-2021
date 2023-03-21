from django.shortcuts import render
import pyrebase
import os
from django.core.files.storage import default_storage
from ADMIN import webscraper
# Create your views here.

config = {"apiKey": "AIzaSyA1DzMKVrhUNojSnnIWrQaYFCEfRI87T00",
          "authDomain": "samarthya-e78f8.firebaseapp.com",
          "databaseURL": "https://samarthya-e78f8-default-rtdb.firebaseio.com",
          "projectId": "samarthya-e78f8",
          "storageBucket": "samarthya-e78f8.appspot.com",
          "messagingSenderId": "511803902375",
          "appId": "1:511803902375:web:74ecd26c37b6f68fb98e82",
          "measurementId": "G-W635CPLQH3"
          }

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


def passwordPage(request):
    if(request.method == 'POST'):
        password = request.POST.get("password")
        print(password)
        if(password != 'codeforgood'):
            return render(request, "admin_password.html")
        print("this should work")
        return render(request, "get_state.html")
    return render(request, "admin_password.html")


def state(request):
    if request.method == "POST":
        state = request.POST.get("state")
    request.session["State"] = state
    circulars = dict(database.child(state).get().val())
    types = []
    names = []
    paths = []
    for keys, value in circulars.items():
        for v in value.values():
            types.append(keys)
            names.append(v['info'])
            paths.append(v['path'])
    combi = zip(names, types, paths)
    return render(request, "admin.html", {"combi": combi})


def fileupload(request):
    if request.method == "POST":
        circular_info = request.POST.get("announcement")
        types = request.POST.get("radio-group")
        file = request.FILES['chooseFile']
        i = file.name.rindex(".")
        exten = file.name[i:]
        newname = circular_info + exten
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = BASE_DIR + '/ADMIN/static/pdf/' + newname
        file_save = default_storage.save(path, file)
        data = {"info": circular_info, "path": newname}
        database.child(request.session['State']).child(types).push(data)
        message = "File was uploaded successfully!!"
        return render(request, "fileupload.html", {"message": message})
    return render(request, "fileupload.html")


def weblinks(request):
    zip1 = webscraper.ndmc()
    zip2 = webscraper.sims()
    return render(request, "links.html", {"zip1": zip1, "zip2": zip2})
