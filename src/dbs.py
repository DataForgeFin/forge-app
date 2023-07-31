from typing import Optional

import pymongo

from src.settings import Settings


def get_mongo_db(database: Optional[str] = None):
    settings = Settings()
    client = pymongo.MongoClient(settings.mongo_uri)
    db = client[database or settings.mongo_db]
    return db
