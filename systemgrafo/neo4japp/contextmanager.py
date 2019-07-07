# -*- coding: utf-8 -*-

from contextlib import contextmanager
# from neo4j.v1 import GraphDatabase, basic_auth, TRUST_DEFAULT (DESCONTINUADO)
from neo4j import GraphDatabase, basic_auth, TRUST_DEFAULT


class Neo4jDBSessionManager:

    """
    Every new connection is a transaction. To minimize new connection overhead for many reads we try to reuse a single
    connection. If this seem like a bad idea some kind of connection pool might work better.
    Neo4jDBConnectionManager.read()
    When using with Neo4jDBConnectionManager.read(): we will always rollback the transaction. All exceptions will be
    thrown.
    Neo4jDBConnectionManager.write()
    When using with Neo4jDBConnectionManager.write() we will always commit the transaction except when we see an
    exception. If we get an exception we will rollback the transaction and throw the exception.
    Neo4jDBConnectionManager.transaction()
    When we don't want to share a connection (transaction context) we can set up a new connection which will work
    just as the write context manager above but with it's own connection.
    >>> manager = Neo4jDBConnectionManager("http://localhost:7474")
    >>> with manager.write() as w:
    ...     w.execute("CREATE (TheMatrix:Movie {title:'The Matrix', tagline:'Welcome to the Real World'})")
    ...
    <neo4j.cursor.Cursor object at 0xb6fafa4c>
    >>>
    >>> with manager.read() as r:
    ...     for n in r.execute("MATCH (n:Movie) RETURN n LIMIT 1"):
    ...         print n
    "({'tagline': 'Welcome to the Real World', 'title': 'The Matrix'},)"
    Commits in batches can be achieved by:
    >>> with manager.write() as w:
    ...     w.execute("CREATE (TheMatrix:Movie {title:'The Matrix Reloaded', tagline:'Free your mind.'})")
    ...     w.connection.commit()  # The Matric Reloaded will be committed
    ...     w.execute("CREATE (TheMatrix:Movie {title:'Matrix Revolutions', tagline:'Everything that has a beginning has an end.'})")
    """

    def __init__(self, uri, username=None, password=None, encrypted=True):
        self.uri = uri
        self.driver = self._get_db_driver(uri, username, password, encrypted)

    @staticmethod
    def _get_db_driver(uri, username=None, password=None, encrypted=True, max_pool_size=50, trust=TRUST_DEFAULT):
        """
        :param uri: Bolt uri
        :type uri: str
        :param username: Neo4j username
        :type username: str
        :param password: Neo4j password
        :type password: str
        :param encrypted: Use TLS
        :type encrypted: Boolean
        :param max_pool_size: Maximum number of idle sessions
        :type max_pool_size: Integer
        :param trust: Trust cert on first use (0) or do not accept unknown cert (1)
        :type trust: Integer
        :return: Neo4j driver
        :rtype: neo4j.v1.session.Driver
        """
        return GraphDatabase.driver(uri, auth=basic_auth(username, password), encrypted=encrypted,
                                    max_pool_size=max_pool_size, trust=trust)

    @contextmanager
    def _session(self):
        session = self.driver.session()
        try:
            yield session
        except Exception as e:
            raise e
    session = property(_session)

    @contextmanager
    def _transaction(self):
        session = self.driver.session()
        transaction = session.begin_transaction()
        try:
            yield transaction
        except Exception as e:
            session.rollback_transaction()
            raise e
        else:
            session.commit_transaction()
    transaction = property(_transaction)

'''
    @contextmanager
    def _transaction(self):
        connection = connect(self.dsn)
        cursor = connection.cursor()
        try:
            yield cursor
        except self.connection.Error as e:
            connection.rollback()
            raise e
        else:
            connection.commit()
        finally:
            cursor.close()
            connection.close()
    transaction = property(_transaction)

    @contextmanager
    def _write(self):
        cursor = self.connection.cursor()
        try:
            yield cursor
        except self.connection.Error as e:
            cursor.close()
            self.connection.rollback()
            raise e
        else:
            cursor.close()
            self.connection.commit()
        finally:
            pass
    write = property(_write)
'''