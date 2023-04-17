FROM python:3.11.2-alpine3.17 as base
COPY requirements.txt .
RUN pip install -r requirements.txt
FROM base
COPY app.py /app/app.py
WORKDIR /app
EXPOSE 5000
ENTRYPOINT  opentelemetry-instrument --traces_exporter otlp,console  --metrics_exporter otlp,console  --service_name lasso-client --exporter_otlp_endpoint "http://otel-collector:4317" flask run --host=0.0.0.0

