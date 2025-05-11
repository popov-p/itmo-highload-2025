from prometheus_client import Counter, Gauge

INSTANT_RULES_COUNTER = Counter('instant_rules_total', 'Total number of instant rules processed')
ONGOING_RULES_COUNTER = Counter('ongoing_rules_total', 'Total number of ongoing rules processed')

CPU_USAGE = Gauge('service_cpu_usage_percent', 'CPU usage in percent')
MEM_USAGE = Gauge('service_mem_usage_percent', 'RAM usage in percent')
# UNAVAILABILITY_DURATION = Gauge('service_unavailable_duration_seconds', 'Time in seconds that the service is unavailable')