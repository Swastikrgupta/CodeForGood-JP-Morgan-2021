import PyPDF2
import pyttsx3
from django.http import request
from django.shortcuts import render, redirect
import pyrebase
import requests
import os
import keyboard
from englisttohindi.englisttohindi import EngtoHindi
from gtts import gTTS
from playsound import playsound

# Create your views here.
config = {
    'apiKey': "AIzaSyA1DzMKVrhUNojSnnIWrQaYFCEfRI87T00",
    'authDomain': "samarthya-e78f8.firebaseapp.com",
    'databaseURL': "https://samarthya-e78f8-default-rtdb.firebaseio.com",
    'projectId': "samarthya-e78f8",
    'storageBucket': "samarthya-e78f8.appspot.com",
    'messagingSenderId': "511803902375",
    'appId': "1:511803902375:web:74ecd26c37b6f68fb98e82",
    'measurementId': "G-W635CPLQH3"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


def chooseUser(request):
    if(request.method == 'POST'):
        user = request.POST.get("user")
        if(user == "Parent"):
            request.session["user"] = "Parent"
            return redirect("Parent")
        request.session["user"] = "Admin"
        return redirect("Admin")
    return render(request, "choose_user.html")


def Parent(request):
    return render(request, "choose_language.html")


def Admin(request):
    return render(request, "admin_password.html")


def chooseState(request):
    if request.method == "POST":
        state = request.POST.get("state")
        request.session["state"] = state
        if request.session["user"] == "Parent":
            circulars = dict(database.child(
                request.session['state']).get().val())
            types = []
            names = []
            paths = []
            for keys, value in circulars.items():
                for v in value.values():
                    types.append(keys)
                    names.append(v['info'])
                    paths.append(v['path'])
            combi = zip(names, types, paths)
            return render(request, "parent.html", {"combi": combi})
        return render(request, "admin.html")
    return render(request, "choose_state.html")


def openpdf(request, path):
    print(path)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = BASE_DIR + '/ADMIN/static/pdf/abcd.pdf'
    return render(request, "test.html", {"path": path})


def read_pdf(request):
    if request.method == "POST":
        req_path = request.POST.get("path")
        mode = request.POST.get("buttonstart")
        print(mode)
        print(req_path)
    path = open(req_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(path)
    from_page = pdfReader.getPage(1)
    text = from_page.extractText()

    # print(text)

    speak = pyttsx3.init()
    if mode == "Stop":
        def onWord(name, location, length):
            print('word', name, location, length)
            if keyboard.is_pressed("esc"):
                speak.stop()
            speak.connect('started-word', onWord)
    elif mode == "Start Reading(Hindi)":
        res = EngtoHindi(text)
        hindi = res.convert
        obj = gTTS(text=hindi, slow=False, lang="hi")
        obj.save("hindi1.mp3")
        playsound('hindi1.mp3')

    else:
        speak.say(text)
        speak.runAndWait()
    print("enter")
    return render(request, "test.html", {"path": req_path})
