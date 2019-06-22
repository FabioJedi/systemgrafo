# Create your views here.
from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Gene, Person
from systemgrafo import db


class GeneDetailView(DetailView):

    model = Gene


class GeneListView(ListView):

    model = Gene


class PersonDetailView(DetailView):

    model = Person


class PersonListView(ListView):

    model = Person


def index(request):
    return render(request, 'neo4japp/index.html')
