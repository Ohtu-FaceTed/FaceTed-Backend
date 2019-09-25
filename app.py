import argparse
import data.data as data
from flask import Flask, escape, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#could be moved to its own module
def next_question():
    attributes = data.attributes()
    id = list(attributes.keys())[0]
    return {"attribute_id": str(id), "attribute_name": attributes.get(id)}

@app.route("/")
def index():
    name = request.args.get("name", "World")
    return "Hello, {escape(name)}"

@app.route('/answer', methods=['POST'])
def answer():
    try:
        content = request.get_json()
        language = content['language']
        attribute_id = content['attribute_id']
        response = content['response']
    except TypeError as e:
        return jsonify({'success': False,
                'message': 'Please supply "language", "attribute_id", and "response" in query'})
    except KeyError as e:
        return jsonify({'success': False,
                'message': 'Please supply "language", "attribute_id", and "response" in query'})
    else:
        return jsonify({'success': True,
                'new_question': {'attribute_id': '0102', 'attribute_name': 'Eteinen'},
                'building_classes': [{'class_id': '0110', 'class_name': 'Omakotitalot', 'score': 0.9},
                                     {'class_id': '0320', 'class_name': 'Hotellit', 'score': 0.5},
                                     {'class_id': '1311', 'class_name': 'Väestönsuojat', 'score': 0.1}]})

@app.route('/question', methods=['GET'])
def question():
    return jsonify({'attribute_id': '0101', 'attribute_name': 'Asuinhuone'})

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true', help='start Flask in debug mode (DANGEROUS!)')
    parser.add_argument('--port', default=5000, help='server port')
    parser.add_argument('--host', default='0.0.0.0', help='server host')
    args = parser.parse_args()

    app.run(debug=args.debug, port=args.port, host=args.host)
