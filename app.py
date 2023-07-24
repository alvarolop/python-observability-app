import sys
from prometheus_client import Counter, Gauge, Histogram, Summary
from prometheus_client.exposition import start_http_server
import random
import time
import logging
from flask import Flask

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNTER = Counter('app_requests_total', 'Total number of requests made')
REQUEST_DURATION = Summary('app_request_duration_seconds', 'Request duration in seconds')
ERROR_COUNTER = Counter('app_errors_total', 'Total number of errors')
CURRENT_REQUESTS = Gauge('app_current_requests', 'Current number of active requests')

# Configure logging to send logs to stdout
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
@REQUEST_DURATION.time()
def hello():
    REQUEST_COUNTER.inc()
    time.sleep(random.uniform(0, 0.5))  # Simulate some processing time
    logging.info('A good request occurred!')

    return 'Hello, Prometheus!'

@app.route('/error')
def error():
    ERROR_COUNTER.inc()
    logging.error('An error occurred!')
    raise Exception('Oops, an error occurred!')

if __name__ == '__main__':
    # Start the Prometheus HTTP server to expose metrics
    start_http_server(8000)
    
    # Start the Flask app on port 5000
    app.run(port=5000)