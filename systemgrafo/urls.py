"""systemgrafo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from __future__ import absolute_import

# Static files for development
from django.conf import settings
from django.conf.urls import url
#from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path
import systemgrafo.core.views

from systemgrafo.subscriptions.views import subscribe
from systemgrafo.neo4japp.views import GeneListView, GeneDetailView, ProteinListView, ProteinDetailView #, neo4j


admin.autodiscover()

urlpatterns = [
    path('', systemgrafo.core.views.home),
    path('inscricao/', subscribe),
    path('admin/', admin.site.urls),
    #path('base/', neo4j),

    # Index view
    #url(r'^$', index),
    url(r'^genes/$', GeneListView.as_view(), name='gene-list'),
    url(r'^genes/(?P<pk>[\d]+)/$', GeneDetailView.as_view(), name='gene-detail'),
    url(r'^proteins/$', ProteinListView.as_view(), name='protein-list'),
    url(r'^proteins/(?P<pk>[\d]+)/$', ProteinDetailView.as_view(), name='protein-detail'),
]
