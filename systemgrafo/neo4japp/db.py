from re import escape
from django.conf import settings
from systemgrafo.neo4japp.contextmanager import Neo4jDBSessionManager


manager = Neo4jDBSessionManager(settings.NEO4J_RESOURCE_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)


def get_node(handle_id, label):
    q = 'MATCH (n:%s { handle_id: {handle_id} }) RETURN n' % label  # Ugly hack
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            return record['n']


def delete_node(handle_id, label):
    q = '''
        MATCH (n:%s { handle_id: {handle_id} })
        OPTIONAL MATCH (n)-[r]-()
        DELETE n, r
        ''' % label
    with manager.session as s:
        s.run(q, {'handle_id': handle_id})


def wildcard_search(search_string):
    search_string = '(?i).*%s.*' % escape(search_string)
    q = """
        OPTIONAL MATCH (m:Protein) WHERE m.name =~ {search_string} WITH collect(m) as proteins
        OPTIONAL MATCH (p:Gene) WHERE p.name =~ {search_string} WITH genes, collect(p) as genes
        RETURN proteins, genes
        """
    with manager.session as s:
        result = s.run(q, {'search_string': search_string})
        return list(result)

def get_codif_protein(handle_id):
    q = """
        MATCH (n:Protein {handle_id: {handle_id}})<-[r:CODIF_PROTEIN]-(gene)
        RETURN gene.handle_id
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['gene.handle_id']}

def get_proteins(handle_id):
    q = """
        MATCH (n:Gene {handle_id: {handle_id}})-[r]->(protein)
        RETURN protein.handle_id, COLLECT(r) as relationships
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['protein.handle_id'], 'relationships': record['relationships']}
