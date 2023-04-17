from flask import Flask, request
import requests
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

exporter = OTLPMetricExporter(insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
set_meter_provider(provider)

logger_provider = LoggerProvider(
    resource=Resource.create(
        {
            "service.name": "demo-client",
            "service.instance.id": "1",
        }
    ),
)
set_logger_provider(logger_provider)

exporter = OTLPLogExporter(insecure=True)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)



meter = get_meter_provider().get_meter("client")
counter = meter.create_counter("client.hello_counter")

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)

# Attach OTLP handler to root logger
from flask.logging import default_handler
root = logging.getLogger()
root.addHandler(handler)

@app.route("/hello", methods=["GET"])
def server_request():
    counter.add(1)
    app.logger.info("About to create a metric counter")
    requests.get("http://demo-server:7080/hello",  timeout=1)
    return "Ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


