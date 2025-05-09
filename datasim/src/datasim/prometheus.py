from prometheus_client import Counter, Gauge

REQUESTS_TOTAL = Counter('requests_total', 'Total number of requests sent to the controller', ['status'])
REQUEST_DURATION = Gauge('request_duration_seconds', 'Duration of request to the controller', ['gpu_id'])
REQUESTS_FAILED = Counter('requests_failed', 'Total number of failed requests', ['gpu_id'])
DEVICE_COUNT = Gauge('device_count', 'Current number of devices sending data to the controller')
DEVICE_FREQ = Gauge('frequency', 'Current frequency of message sening, Hz')