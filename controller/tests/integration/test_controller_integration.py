import requests
import pytest

@pytest.mark.integration
def test_post_binary_protobuf(fixed_batch):
    url = "http://localhost:8060/incoming-data"

    binary_data = fixed_batch.SerializeToString()

    response = requests.post(url, data=binary_data)

    assert response.status_code == 200

@pytest.mark.integration
def test_post_empty_body():
    url = "http://localhost:8060/incoming-data"

    response = requests.post(url, data=b"")

    assert response.status_code == 500
    assert "request body is empty" in response.text.lower()

@pytest.mark.integration
def test_get_report():
    url = "http://localhost:8060/report"

    response = requests.post(url, data=b"")

    assert response.status_code == 405