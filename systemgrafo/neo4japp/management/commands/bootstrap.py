# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.management.base import BaseCommand
from django.db import DatabaseError
import uuid
from systemgrafo.neo4japp.models import Protein, Gene
from systemgrafo.neo4japp import db


class Command(BaseCommand):
    help = 'Create a NodeHandle and set handle_id for nodes missing handle_id property'

    def handle(self, *args, **options):
        with db.manager.session as s:
            s.run('CREATE CONSTRAINT ON (p:Gene) ASSERT p.handle_id IS UNIQUE')
            s.run('CREATE CONSTRAINT ON (m:Protein) ASSERT m.handle_id IS UNIQUE')

            try:
                q = """
                    OPTIONAL MATCH (m:Protein) WHERE NOT exists(m.handle_id) WITH collect(id(m)) as Proteins
                    OPTIONAL MATCH (p:Gene) WHERE NOT exists(p.handle_id) WITH proteins, collect(id(p)) as genes
                    RETURN proteins, genes
                    """

                record = s.run(q).single()
                proteins = record['proteins']
                genes = record['genes']
            except IndexError:
                proteins, genes = [], []

        q = 'MATCH (n) WHERE ID(n) = $node_id SET n.handle_id = $handle_id'
        m, p = 0, 0
        protein_objs = []
        gene_objs = []
        with db.manager.transaction as t:
            try:
                for node_id in proteins:
                    protein = Protein(handle_id=str(uuid.uuid4()))
                    protein_objs.append(protein)
                    t.run(q, {'node_id': node_id, 'handle_id': movie.handle_id})
                    m += 1
            except Exception as e:
                raise e
            else:
                try:
                    Protein.objects.bulk_create(protein_objs)
                except DatabaseError as e:
                    raise e

        with db.manager.transaction as t:
            try:
                for node_id in genes:
                    gene = Gene(handle_id=str(uuid.uuid4()))
                    gene_objs.append(gene)
                    t.run(q, {'node_id': node_id, 'handle_id': gene.handle_id})
                    p += 1
            except Exception as e:
                raise e
            else:
                try:
                    Gene.objects.bulk_create(gene_objs)
                except DatabaseError as e:
                    raise e

        self.stdout.write('Successfully completed! Added %d proteins and %d genes.' % (m, p))
