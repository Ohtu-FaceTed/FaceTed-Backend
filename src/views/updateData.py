from flask import request
from . import views as app
from .. import building_data, classifier


@app.route("/update", methods=["GET"])
def update():
    try:
        building_data.load_from_db()
        print("woop!")
        classifier.load_from_db()
        print("woopx2!")
    except:
        print("it all went to hell")

    return ('', 204)
