import argparse
from flask import Flask, escape, request

app = Flask(__name__)


@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"

@app.route('/answer', methods=['POST'])
def answer():
    return {'new_question': {'attribute_id': 101, 'attribute_fi': 'Asuinhuone'},
            'building_classes': [{'class_id': 110, 'class_fi': 'Omakotitalot', 'score': 0.9},
                                 {'class_id': 320, 'class_fi': 'Hotellit', 'score': 0.5},
                                 {'class_id': 1311, 'class_fi': 'Väestönsuojat', 'score': 0.1}]}

@app.route('/question', methods=['GET'])
def question():
    return {'attribute_id': 101, 'attribute_fi': 'Asuinhuone'}

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true', help='start Flask in debug mode (DANGEROUS!)')
    args = parser.parse_args()

    app.run(debug=args.debug)
