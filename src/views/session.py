from flask import render_template, request
from flask_login import login_required
from sqlalchemy import func

from . import views as app
from ..models import db, AnswerQuestion, Session


# results view
@app.route("/801fc3r", methods=["GET"])
@login_required
def results_view():
    # Change default_minimum to 0 if you want to always see empty sessions by default, or some other number if you want the filtering to be rougher.
    # For a quick temporary filter- In the browser, you can use /801fc3r?min=5 for example, to set the filter to only show sessions with 5 or more answered questions
    default_minimum = 1
    count = request.args.get('min')
    try:
        if count:
            count = max(int(count), default_minimum)
        else:
            count = default_minimum
    except:
        count = default_minimum

    return render_template("resultsView.html", sessions=Session.query
                           .outerjoin(AnswerQuestion)
                           .group_by(Session)
                           .having(func.count_(Session.answered_questions) >= count)
                           .all()
                           )


@app.route("/801fc3s", methods=["GET"])
@login_required
def session_view():
    session_id = request.args.get('session')

    sess = Session.query.get(session_id)
    return render_template("sessionView.html", session=sess)
