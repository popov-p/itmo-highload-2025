import pytest
from unittest import mock

@pytest.fixture
def mock_instant_insert():
    with mock.patch('rule_engine.database.instant.insert_one') as mock_insert:
        return mock_insert

@pytest.fixture
def mock_ongoing_insert():
    with mock.patch('rule_engine.database.ongoing.insert_one') as mock_insert:
        return mock_insert

@pytest.fixture
def mock_current_id_stack_insert():
    with mock.patch('rule_engine.database.insert_one') as mock_insert:
        return mock_insert

@pytest.fixture
def mock_db_drop_collection():
    with mock.patch('rule_engine.database.db.drop_collection') as mock_drop:
        return mock_drop

@pytest.fixture
def mock_message():
    class MockMessage:
        def __init__(self, body):
            self.body = body
            self.channel = mock.Mock()
            self.delivery_tag = 'test_tag'

    return MockMessage

@pytest.fixture
def mock_batch():
    batch = mock.Mock()
    batch.gpu_info.max_ker_temp = 80
    batch.gpu_info.gpu_id = 'gpu_1'
    batch.ker_temp = 85
    batch.mem_temp = 75
    batch.timestamp = str(1234567890)
    return batch


@pytest.fixture
def mock_valid_batch():
    batch = mock.Mock()
    batch.gpu_info.max_ker_temp = 93
    batch.gpu_info.gpu_id = 'gpu_1'
    batch.ker_temp = 85
    batch.mem_temp = 75
    batch.timestamp = str(1234567890)
    return batch