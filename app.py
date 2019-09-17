import argparse
from flask import Flask, escape, request

app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true', help='start Flask in debug mode (DANGEROUS!)')
    args = parser.parse_args()

    app.run(debug=args.debug)
