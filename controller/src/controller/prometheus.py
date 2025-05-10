from prometheus_client import Counter

REQUESTS = Counter('requests_total', 'Total number of requests sent to the controller')
