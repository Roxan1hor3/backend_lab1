from backend import app


@app.route("/healthcheck/")
def hello_world():
    return "<p>Hello, World!</p>"
