import src
from src import app
import argparse


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Run Faceted-Search Flask backend')
    parser.add_argument('--debug', action='store_true',
                        help='start Flask in debug mode (DANGEROUS!)')
    parser.add_argument('--port', default=5000, help='server port')
    parser.add_argument('--host', default='0.0.0.0', help='server host')
    parser.add_argument('--data_directory',
                        default='./data', help='data directory')
    args = parser.parse_args()

    # Load data from the supplied directorytand replace the default objects
    src.building_data = src.BuildingData(args.data_directory)
    src.classifier = src.NaiveBayesClassifier(src.building_data.observations)

    app.run(debug=args.debug, port=args.port, host=args.host)
