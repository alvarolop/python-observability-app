import sys
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import Counter, Gauge, Histogram, Summary, multiprocess, generate_latest
from prometheus_client import make_wsgi_app
import random
import time
import logging
from flask import Flask, Response, render_template

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNTER = Counter('app_requests_total', 'Total number of requests made')
APP_HELLO_COUNTER = Counter('app_hello_counter_total', 'Total requests made to hello endpoint')
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
def web_interface():
    total_requests = REQUEST_COUNTER._value.get()
    total_hellos = APP_HELLO_COUNTER._value.get()
    total_errors = ERROR_COUNTER._value.get()
    return render_template('index.html', total_requests=total_requests, total_hellos=total_hellos, total_errors=total_errors)

@app.route('/hello')
@REQUEST_DURATION.time()
def hello():
    REQUEST_COUNTER.inc()
    APP_HELLO_COUNTER.inc()
    time.sleep(random.uniform(0, 0.5))  # Simulate some processing time
    logging.info('A good request occurred!')

    return 'Hello, Prometheus!'

@app.route('/error')
def error():
    REQUEST_COUNTER.inc()
    ERROR_COUNTER.inc()
    logging.error('An error occurred!')
    raise Exception('Oops, an error occurred!')

@app.route('/health/live')
def live():
    return 'Live and responsive!', 200

@app.route('/health/ready')
def ready():
    # Add readiness checks here (e.g., database connections, external services)
    # Return 200 if the app is ready, otherwise return a non-200 status code
    return 'Ready to accept requests!', 200

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':  
    # Start the Flask app on port 5000 together with Prometheus HTTP server to expose metrics
    app.run(host='0.0.0.0', port=8080)
