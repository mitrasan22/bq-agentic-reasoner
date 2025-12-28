import os
from google.cloud import firestore


class FirestoreClient:
    _client = None
    _database = None

    @classmethod
    def get(cls):
        database = os.getenv("FIRESTORE_DATABASE")
        if cls._client is None or cls._database != database:
            if database:
                cls._client = firestore.Client(database=database)
            else:
                cls._client = firestore.Client()

            cls._database = database

        return cls._client
