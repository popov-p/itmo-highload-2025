import pytest
from rule_engine.rabbitmq import on_message

@pytest.mark.unit
def test_add():
    assert 1 + 1 == 2

async def test_on_message_exceeds_ker_temp(mock_message,
                                           mock_batch,
                                           mock_instant_insert,
                                           mock_ongoing_insert,
                                           mock_db_drop_collection):

    mock_instant_insert.return_value = None
    mock_ongoing_insert.return_value = None

    await on_message(mock_message)

    mock_instant_insert.assert_called_once()
    mock_db_drop_collection.assert_called_once()


async def test_valid_temperatures(mock_message,
                                  mock_valid_batch,
                                  mock_instant_insert,
                                  mock_ongoing_insert,
                                  mock_db_drop_collection):

    mock_instant_insert.return_value = None

    await on_message(mock_message)

    mock_ongoing_insert.assert_called_once()
