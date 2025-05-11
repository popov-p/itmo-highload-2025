import pytest
from unittest import mock
from controller.app import app
from fastapi import FastAPI
from fastapi.testclient import TestClient
from controller.database import db
from controller.router import router
from proto.messages_pb2 import Batch
from fastapi import Request, HTTPException

@pytest.fixture
def mock_db_insert():
    with mock.patch('controller.database.db.data.insert_one') as mock_insert:
        return mock_insert

@pytest.fixture
def mock_create_channel_for_device():
    with mock.patch('controller.rabbitmq_utils.create_channel_for_device') as mock_create_channel:
        return mock_create_channel


@pytest.fixture
def client():
    test_app = FastAPI()

    @test_app.post("/incoming-data")
    async def mock_incoming_data(request: Request):
        batch = Batch()
        body = await request.body()
        if not body:
            raise HTTPException(status_code=500, detail="Empty request body")

        try:
            batch.ParseFromString(body)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to parse request body") from e

        return {"status": "Ok"}

    @test_app.get("/report")
    async def mock_report():
        detailed_report = {
            "gpu_info": {
                "avg_ker_temp": 75.5,
                "avg_ker_load": 65.2,
                "avg_mem_temp": 80.3,
                "avg_mem_load": 70.1,
                "ker_temps": [70.0, 75.0, 80.0, 78.0],
                "ker_loads": [60.0, 65.0, 70.0, 68.0],
                "mem_temps": [75.0, 80.0, 85.0, 82.0],
                "mem_loads": [65.0, 70.0, 75.0, 72.0],
            }
        }
        return detailed_report

    return TestClient(test_app)

