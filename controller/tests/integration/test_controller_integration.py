import requests
import pytest
import base64

# @pytest.mark.integration
# def test_post_binary_protobuf(fixed_batch):
#     url = "http://localhost:8060/incoming-data"
#
#     binary_data = fixed_batch.SerializeToString()
#     encoded = base64.b64encode(binary_data).decode('ascii')
#
#     response = requests.post(url, data=encoded)
#
#     assert response.status_code == 200
#
# @pytest.mark.integration
# def test_post_empty_body():
#     url = "http://localhost:8060/incoming-data"
#
#     response = requests.post(url, data=b"")
#
#     assert response.status_code == 500
#     assert "request body is empty" in response.text.lower()
#
# @pytest.mark.integration
# def test_get_report():
#     url = "http://localhost:8060/report"
#
#     response = requests.get(url, data=b"")
#
#     assert response.status_code == 405