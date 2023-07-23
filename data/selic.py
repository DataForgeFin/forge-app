import datetime

import pymongo

from src.settings import Settings


def get_selic(start_date, end_date=datetime.datetime.now()):
    settings = Settings()
    client = pymongo.MongoClient(settings.mongo_uri)
    db = client[settings.mongo_db]
    collection = db.finance_metrics_daily
    query = {"date": {"$gte": start_date, "$lte": end_date}}
    result = collection.find(query)
    return result
