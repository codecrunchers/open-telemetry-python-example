Simple app forked from OTL and update to use an auto instrumented python client


Services
 - Jaeger (Tracing, Exception Logging) http://localhost:16686/
 - Python Flask Client, auto-instrumented http://localhost:5000/hello
 - OTEL Collector 
 - Prometheus, metrics http://localhost:9090, scrapes from OTEL:
