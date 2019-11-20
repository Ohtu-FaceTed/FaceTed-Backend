from . import views as app
from ..models import db, Answer, AnswerQuestion, Attribute, Session
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required

@app.route("/801fc3", methods=["GET"])
@login_required
def admin_view():
    return render_template("admView.html", attributes=Attribute.query.all())


@app.route("/de95b/<attribute_id>", methods=["POST"])
@login_required
def setActive(attribute_id):
    attr = Attribute.query.get(attribute_id)

    if attr.active:
        attr.active = False
    else:
        attr.active = True
        db.session.commit()
    return redirect(url_for("views.admin_view"))
