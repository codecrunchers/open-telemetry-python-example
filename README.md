Simple app forked from OTL and updated to use an auto instrumented python client

This auto instruments a Python Application for distributed tracing. Configures it for metric and logs exports with minimal code. An OTEL Collector sits in between the Apps , (There is a Go Server & a Python Client) and then exports this OTLP format data to the awaiting clients. 

![Sample Arch](./docs/demo-arch.png)
source:OTEL Examples Repo

### Run
```
docker-compose up -d
```
Hit the Client End point and then access the various tracing Services below to see Logs, Metrics & Dist Traces

### Run Python app locally

Create a virt env
```
python -m pip install -r requirements.txt
cd client
flask run #(or use cmd from Dockerfile)
```

The requirements are mostly auto-generated, you add Flask /  Django then run the instrumenter for necessary libs. 


### Services
 - Jaeger (Tracing, Exception Logging) http://localhost:16686/
 - Python Flask Client, auto-instrumented http://localhost:5000/hello
 - OTEL Collector Contrib (with logging pre release)
 - Prometheus, metrics http://localhost:9090
 - Grafana / Loki for App Logging http://localhost:3000 (Add loki on loki:3100  as Loki Data Source, and Prom on 9090 if you want)

## Screenshots


![Jaeger Traces](./docs/Jaeger.png)
![Prometheus metrics](./docs/Prometheus.png)
![Loki - Grafana](./docs/Grafana-Logs.png)
![Prometheus Data Sources - Grafana](./docs/Grafana-Prom.png)

