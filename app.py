import argparse, random
import data.data as data
from flask import Flask, escape, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#could be moved to its own module
def next_question():
    id = random.choice(list(data.attributes.keys()))
    return {"attribute_id": str(id), "attribute_name": data.attributes.get(id)}

@app.route("/")
def index():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)}"

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
        posterior = data.calculate_posterior(attribute_id, response)
        new_building_classes = []
        for ind,(class_id, score) in posterior.iterrows():
            new_building_classes.append({'class_id': class_id, 
                                         'class_name': data.building_classes[class_id],
                                         'score': score})

        return jsonify({'success': True,
                'new_question': next_question(),
                'building_classes': new_building_classes})

@app.route('/question', methods=['GET'])
def question():
    return jsonify(next_question())

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true', help='start Flask in debug mode (DANGEROUS!)')
    parser.add_argument('--port', default=5000, help='server port')
    parser.add_argument('--host', default='0.0.0.0', help='server host')
    args = parser.parse_args()

    app.run(debug=args.debug, port=args.port, host=args.host)
