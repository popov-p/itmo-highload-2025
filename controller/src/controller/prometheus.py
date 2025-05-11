from prometheus_client import Counter, Gauge

REQUESTS = Counter('requests_total', 'Total number of requests sent to the controller')

CPU_USAGE = Gauge('service_cpu_usage_percent', 'CPU usage in percent')
MEM_USAGE = Gauge('service_mem_usage_percent', 'RAM usage in percent')

# UNAVAILABILITY_DURATION = Gauge('service_unavailable_duration_seconds', 'Time in seconds that the service is unavailable')