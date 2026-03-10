# gunicorn.conf.py

wsgi_app = "wsgi:app"

bind = "127.0.0.1:8181"
backlog = 2048

workers = 1
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50

timeout = 30
graceful_timeout = 30
keepalive = 5

limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

accesslog = "-"
errorlog = "-"
loglevel = "info"

preload_app = True
