import requests
from pymongo import MongoClient
import pytest
import time
@pytest.mark.integration
def test_post_and_check_mongo(fixed_batch):
    binary_data = fixed_batch.SerializeToString()

    url = "http://localhost:8060/incoming-data"
    headers = {"Content-Type": "application/octet-stream"}
    requests.post(url, data=binary_data, headers=headers)


    client = MongoClient("mongodb://pavel:popov@localhost:27017/")
    db = client["iotdata"]
    collection = db["instant"]

    time.sleep(2)

    count = collection.count_documents({})
    assert count > 0, "Коллекция пуста, записи не найдены"

@pytest.mark.integration
def test_send_multiple_batches_with_same_gpu_id(make_batch):
    gpu_id = 99  # одинаковый ID
    url = "http://localhost:8060/incoming-data"
    headers = {"Content-Type": "application/octet-stream"}

    timestamps = []
    for _ in range(10):
        batch = make_batch(gpu_id=gpu_id)
        timestamps.append(batch.timestamp)
        binary_data = batch.SerializeToString()
        requests.post(url, data=binary_data, headers=headers)

    time.sleep(2)
    
    client = MongoClient("mongodb://pavel:popov@localhost:27017/")
    db = client["iotdata"]
    ongoing_collection = db["ongoing"]


    count = ongoing_collection.count_documents({})
    assert count > 0