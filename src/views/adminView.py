import json
from . import views as app
from ..models import db, Answer, AnswerQuestion, Attribute, Session
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required


@app.route("/801fc3", methods=["GET"])
@login_required
def admin_view():
    return render_template("admView.html", attributes=Attribute.query.all())


# question string edit
@app.route("/editQuestionString/<attribute_id>", methods=["GET"])
@login_required
def edit_question_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_question)
    # Remember to edit the post_url to be the correct endpoint!
    # Otherwise, it should be pretty straight forward to copy-paste this GET method, and the POST method for edit_question_string
    # And then just edit out which json to be edited, and where to post, and maybe where to redirect if required.
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'), 
                           post_url=url_for('views.edit_question_string', attribute_id=attr.id) )


#question string edit post handler
@app.route("/edit_question_string/<attribute_id>", methods=["POST"])
@login_required
def edit_question_string(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        jsoned = json.loads(attr.attribute_question)

        # Once the old data has been loaded, check that new data is not empty. If not empty, change the new data.
        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        # Then save the new data into the attribute_question as json.
        attr.attribute_question = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing gone goofed')

    return redirect(url_for("views.admin_view"))


#attribute name edit
@app.route("/editAttributeName/<attribute_id>", methods=["GET"])
@login_required
def edit_attribute_name_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_name)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'), 
                           post_url=url_for('views.edit_attribute_name', attribute_id=attr.id) )


#attribute name edit post handler
@app.route("/edit_attribute_name/<attribute_id>", methods=["POST"])
@login_required
def edit_attribute_name(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        jsoned = json.loads(attr.attribute_name)

        # Once the old data has been loaded, check that new data is not empty. If not empty, change the new data.
        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        # Then save the new data into the attribute_question as json.
        attr.attribute_name = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing failed in attribute_name_edit')

    return redirect(url_for("views.admin_view"))


#results view
@app.route("/801fc3r", methods=["GET"])
@login_required
def results_view():
    return render_template("resultsView.html", sessions=Session.query.all())


# session list view
@app.route("/801fc3s", methods=["GET"])
@login_required
def session_view():
    session_id = request.args.get('session')

    sess = Session.query.get(session_id)
    return render_template("sessionView.html", session=sess)


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
