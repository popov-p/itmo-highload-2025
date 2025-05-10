from prometheus_client import Counter

INSTANT_RULES_COUNTER = Counter('instant_rules_total', 'Total number of instant rules processed')
ONGOING_RULES_COUNTER = Counter('ongoing_rules_total', 'Total number of ongoing rules processed')
