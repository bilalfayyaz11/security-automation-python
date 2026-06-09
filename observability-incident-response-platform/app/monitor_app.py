from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
import random
import logging
import os

app = Flask(__name__)

request_count = Counter("app_requests_total", "Total requests", ["method", "endpoint"])
request_duration = Histogram("app_request_duration_seconds", "Request duration")
active_connections = Gauge("app_active_connections", "Active connections")
error_count = Counter("app_errors_total", "Total errors", ["type"])

user = os.environ.get("USER", "ubuntu")
log_file = f"/home/{user}/observability-lab/app.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.route("/")
def home():
    start_time = time.time()
    request_count.labels(method="GET", endpoint="/").inc()
    active_connections.inc()

    logging.info("Request received on / endpoint")
    time.sleep(random.uniform(0.1, 0.5))

    active_connections.dec()
    request_duration.observe(time.time() - start_time)
    return "Application is running!"


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")


@app.route("/health")
def health():
    request_count.labels(method="GET", endpoint="/health").inc()

    if random.random() < 0.1:
        error_count.labels(type="health_check").inc()
        logging.error("Health check failed!")
        return "Unhealthy", 500

    logging.info("Health check passed")
    return "Healthy", 200


@app.route("/load")
def generate_load():
    start_time = time.time()
    request_count.labels(method="GET", endpoint="/load").inc()
    active_connections.inc()

    duration = random.uniform(1, 3)
    logging.info(f"Processing load request for {duration:.2f} seconds")
    time.sleep(duration)

    active_connections.dec()
    request_duration.observe(time.time() - start_time)
    return f"Processed for {duration:.2f} seconds"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
