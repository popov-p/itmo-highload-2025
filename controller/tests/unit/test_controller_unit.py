import pytest
from proto.messages_pb2 import Batch
from unittest import mock
from controller.database import db


@pytest.mark.unit
def test_incoming_data(client, mock_db_insert, mock_create_channel_for_device):
    batch = Batch()
    batch.gpu_info.gpu_id = 1
    batch.ker_temp = 45
    batch.ker_load = 55
    batch.mem_temp = 60
    batch.mem_load = 70
    batch.timestamp = str(1624902442)

    mock_db_insert.return_value.inserted_id = 'test_id'

    mock_create_channel_for_device.return_value.basic_publish = mock.MagicMock()

    assert batch.gpu_info.gpu_id == 1
    assert batch.ker_temp == 45
    assert batch.ker_load == 55
    assert batch.mem_temp == 60
    assert batch.mem_load == 70
    assert batch.timestamp == str(1624902442)

    response = client.post("/incoming-data", content=batch.SerializeToString())

    assert response.status_code == 200
    assert response.json() == {"status": "Ok"}

@pytest.mark.unit
def test_incoming_data_empty_body(client):
    response = client.post("/incoming-data", content=b'')

    assert response.status_code == 500
    assert response.json() == {"detail": "Empty request body"}

@pytest.mark.unit
def test_incoming_data_invalid_string(client):
    response = client.post("/incoming-data", content=b'Invalid string data')

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to parse request body"}


@pytest.mark.unit
def test_mock_report(client):
    response = client.get("/report")

    assert response.status_code == 200
    assert response.json() == {
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
