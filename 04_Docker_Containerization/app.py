from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    raise RuntimeError("V2 crashes!")


    return jsonify(
        message="Hello from a containerized Flask app!",
        environment=os.getenv("APP_ENV", "development")
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
