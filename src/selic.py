import datetime
from typing import Any, Dict, List

from src.dbs import get_mongo_db


def get_selic(start_date, end_date=datetime.datetime.now()) -> List[Dict[str, Any]]:
    db = get_mongo_db()
    collection = db.finance_metrics_daily
    query = {"date": {"$gte": start_date, "$lte": end_date}, "metadata.metric": "selic"}
    result = list(collection.find(query))
    return [{"date": f["date"], "value": f["value"]} for f in result]
