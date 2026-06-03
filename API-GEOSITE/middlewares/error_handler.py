from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Pass through HTTP errors
        if isinstance(e, HTTPException):
            return jsonify({
                "error": e.name,
                "message": e.description,
                "code": e.code
            }), e.code

        # Handle non-HTTP exceptions only in production or as generic error
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e) if app.debug else "An unexpected error occurred.",
            "code": 500
        }), 500
