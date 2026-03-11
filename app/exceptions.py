from flask import Flask, render_template, request


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):
        app.logger.warning("404 Not Found: %s %s", request.method, request.path)
        return render_template("errors/404.html"), 404

    @app.errorhandler(Exception)
    def internal_error(error):
        app.logger.error("500 Internal Server Error: %s %s - %s", request.method, request.path, error, exc_info=True)
        return render_template("errors/500.html"), 500
