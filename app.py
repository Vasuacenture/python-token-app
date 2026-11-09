"""Flask application for generating labeled identification tokens."""

import os
import secrets

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.get("/")
def index():
    """Render the token generator form."""
    return render_template("index.html")


@app.post("/api/token")
def create_token():
    """Validate a label and return a newly generated token as JSON."""
    if not request.is_json:
        return jsonify(success=False, error="Send the request as JSON."), 415

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify(success=False, error="The JSON body must be an object."), 400

    label = data.get("label")
    if not isinstance(label, str):
        return jsonify(success=False, error="A label is required."), 400

    label = label.strip()
    if not label:
        return jsonify(success=False, error="A label is required."), 400
    if len(label) > 100:
        return jsonify(success=False, error="The label must be 100 characters or fewer."), 400

    # Generate an unpredictable URL-safe token rather than using random identifiers.
    token = secrets.token_urlsafe(32)
    return jsonify(success=True, label=label, token=token), 201


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    """Keep HTTP errors from the API in the same JSON response format."""
    if request.path == "/api/token":
        return jsonify(success=False, error=error.description), error.code
    return error


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG") == "1",
    )
