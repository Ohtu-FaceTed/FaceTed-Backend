import json
from . import views as app
from ..models import db, Answer, AnswerQuestion, Attribute, BuildingClass, Session
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
                           post_url=url_for('views.edit_question_string', attribute_id=attr.id))


# question string edit post handler
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


# attribute name edit
@app.route("/editAttributeName/<attribute_id>", methods=["GET"])
@login_required
def edit_attribute_name_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_name)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'),
                           post_url=url_for('views.edit_attribute_name', attribute_id=attr.id))


# Attribute name edit post handler.
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


# Tooltip edit
@app.route("/editTooltip/<attribute_id>", methods=["GET"])
@login_required
def edit_tooltip_view(attribute_id):
    attr = Attribute.query.get(attribute_id)
    json_a = json.loads(attr.attribute_tooltip)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.admin_view'),
                           post_url=url_for('views.edit_tooltip', attribute_id=attr.id))


# Tooltip edit post handler.
@app.route("/edit_tooltip/<attribute_id>", methods=["POST"])
@login_required
def edit_tooltip(attribute_id):
    attr = Attribute.query.get(attribute_id)

    try:
        form = request.form
        jsoned = json.loads(attr.attribute_tooltip)

        # Once the old data has been loaded, check that new data is not empty. If not empty, change the new data.
        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        # Then save the new data into the attribute_tooltip as json.
        attr.attribute_tooltip = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing failed in attribute_name_edit')

    return redirect(url_for("views.admin_view"))


# Class probability edit post handler.
@app.route("/edit_class_probability/<class_id>", methods=["POST"])
@login_required
def edit_class_probability(class_id):
    b_class = BuildingClass.query.get(attribute_id)
    probability = request.form["probability"]
    if (probability):
        try:
            b_class.class_probability = probability
            db.session.commit()
        except:
            print('Error in editing class probability')

    return redirect(url_for("views.classes_view"))


# Building class create
@app.route("/createBuildingClass", methods=["GET"])
@login_required
def create_building_class_view():
    b_class = vars(db.session.query(BuildingClass).first())
    b_class.pop("_sa_instance_state", None)
    return render_template("createTemplate.html", object=b_class, redirect_url=url_for('views.classes_view'),
                           post_url=url_for('views.create_building_class'))


# Building class create post handler
@app.route("/create_building_class", methods=["POST"])
@login_required
def create_building_class():
    try:
        form = request.form
        db.session.add(BuildingClass(class_id=form["class_id"],
                                                class_name=form["class_name"]))
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()

    return redirect(url_for("views.classes_view"))


# building classes view
@app.route("/801fc3c", methods=["GET"])
@login_required
def classes_view():
    building_classes = BuildingClass.query.all()
    for one in building_classes:
        one.class_name = json.loads(one.class_name)["fi"]
    return render_template("classesView.html", building_classes=building_classes)


# results view
@app.route("/801fc3r", methods=["GET"])
@login_required
def results_view():
    return render_template("resultsView.html", sessions=Session.query.all())


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
