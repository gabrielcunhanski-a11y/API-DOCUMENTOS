import time
from flask import request, g

def register_logger(app):
    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if request.path == '/favicon.ico':
            return response
        
        diff = time.time() - g.start
        status = response.status_code
        method = request.method
        path = request.path
        
        print(f"[{method}] {path} - {status} ({diff:.4f}s)")
        return response
