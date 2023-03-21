"""Samarthya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ADMIN import views as admin_views
from PARENT import views as parent_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('password', admin_views.passwordPage, name="passwordPage"),
    path('links', admin_views.weblinks, name="weblinks"),
    path('circular', admin_views.state, name="state"),
    path('fileupload', admin_views.fileupload, name="fileupload"),
    path('', parent_views.chooseUser, name="chooseUser"),
    path('Parent/', parent_views.Parent, name="Parent"),
    path('Admin', parent_views.Admin, name="Admin"),
    path('State', parent_views.chooseState, name="chooseState"),
    path('openpdf/<str:path>/', parent_views.openpdf, name="openpdf"),
    path('readpdf', parent_views.read_pdf, name="read_pdf")
]
