from django.db import models
# from django.core.urlresolvers import reverse (Descontinuado)
from django.urls import reverse
from systemgrafo.neo4japp import db


# Create your models here.
class NodeHandle(models.Model):
    handle_id = models.CharField(max_length=64, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'NodeHandle for node %d' % self.node()['handle_id']
        
    def node(self):
        return db.get_node(self.handle_id, self.__class__.__name__)

    def delete(self, **kwargs):
        """Delete that node handle and the handles node."""
        db.delete_node(self.handle_id, self.__class__.__name__)
        super(NodeHandle, self).delete()
        return True

    delete.alters_data = True


class Protein(NodeHandle):

    def __str__(self):
        return self.name

    def _name(self):
        try:
            return self.node().properties.get('name', 'Missing title')
        except AttributeError:
            return 'Nó ausente?'
    name = property(_name)

    def get_absolute_url(self):
        return reverse('protein-detail', args=[str(self.id)])

    def _codif_protein(self):
        genes = []
        for gene in db.get_directors(self.handle_id):
            genes.append({'gene': Gene.objects.get(handle_id=gene['handle_id'])})
        return genes
    codif_protein = property(_codif_protein)


class Gene(NodeHandle):

    def __str__(self):
        return self.name

    def _name(self):
        try:
            return self.node().properties.get('name', 'Missing name')
        except AttributeError:
            return 'Nó ausente?'
    name = property(_name)

    def get_absolute_url(self):
        return reverse('gene-detail', args=[str(self.id)])

    def _proteins(self):
        proteins = []
        for protein in db.get_proteins(self.handle_id):
            proteins.append({'protein': Protein.objects.get(handle_id=protein['handle_id']),
                           'relationships': protein['relationships']})
        return proteins
    proteins = property(_proteins)
