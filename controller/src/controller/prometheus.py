from prometheus_client import Counter, Gauge

REQUESTS = Counter('requests_total', 'Total number of requests sent to the controller', ['hostname'])

CPU_USAGE = Gauge('service_cpu_usage_percent', 'CPU usage in percent', ['hostname'])
MEM_USAGE = Gauge('service_mem_usage_percent', 'RAM usage in percent', ['hostname'])
