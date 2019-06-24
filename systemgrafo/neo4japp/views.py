# Create your views here.
from __future__ import absolute_import

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Gene, Protein
from systemgrafo.neo4japp import db


class GeneDetailView(DetailView):

    model = Gene


class GeneListView(ListView):

    model = Gene


class ProteinDetailView(DetailView):

    model = Protein


class ProteinListView(ListView):

    model = Protein


def index(request):
    return render(request, 'neo4japp/base.html')
