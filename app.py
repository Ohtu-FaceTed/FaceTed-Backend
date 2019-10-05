from src import app
import argparse
from flask import Flask, escape, request, jsonify



@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true',
                        help='start Flask in debug mode (DANGEROUS!)')
    parser.add_argument('--port', default=5000, help='server port')
    parser.add_argument('--host', default='0.0.0.0', help='server host')
    args = parser.parse_args()

    app.run(debug=args.debug, port=args.port, host=args.host)
