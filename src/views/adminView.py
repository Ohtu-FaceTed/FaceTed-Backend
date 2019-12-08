import json
from . import views as app
from ..models import db, Answer, AnswerQuestion, Attribute, BuildingClass, ClassAttribute, Session
from flask import redirect, render_template, request, url_for, jsonify, flash
from flask_login import login_required
from sqlalchemy.exc import IntegrityError, StatementError
from sqlalchemy import func


@app.route("/801fc3", methods=["GET"])
@login_required
def admin_view():
    return render_template("admView.html", attributes=Attribute.query.all(), groups = QuestionGroup.query.all())


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
    b_class = BuildingClass.query.get(class_id)
    try:
        b_class.class_probability = request.form["probability"]
        db.session.commit()
    except:
        flash("Probability should be a numeric value.")

    return redirect(url_for("views.classes_view"))


# Building class create
@app.route("/createBuildingClass", methods=["GET"])
@login_required
def create_building_class_view():
    b_class = vars(db.session.query(BuildingClass).first())
    b_class.pop("_sa_instance_state", None)
    b_class.pop("id", None)
    return render_template("createTemplate.html", object=b_class,
                           redirect_url=url_for('views.classes_view'),
                           post_url=url_for('views.create_building_class'),
                           info='Only add building classes that are defined in Statistics Finland API.')


# Building class create post handler
@app.route("/create_building_class", methods=["POST"])
@login_required
def create_building_class():
    form = request.form
    if (not form["class_id"] or not form["class_name"]):
        flash("Fill all the fields.")
        return redirect(url_for("views.create_building_class_view"))
    try:
        name = f'{{"fi":"{form["class_name"]}", "en":"", "sv":""}}'
        b_class = BuildingClass(class_id=form["class_id"],
                                class_name=name,
                                class_probability=form["class_probability"])
        db.session.add(b_class)
        db.session.commit()
        b_class = BuildingClass.query.filter_by(class_id=b_class.class_id).first()
        attributes = Attribute.query.all()
        for one in attributes:
            db.session.add(ClassAttribute(attribute=one, building_class=b_class))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Building class with corresponding class id already exists.")
        return redirect(url_for("views.create_building_class_view"))
    except:
        flash("Probability should be a numeric value.")
        return redirect(url_for("views.create_building_class_view"))

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


@app.route("/gs59e/<attribute_id>", methods=["POST"])
@login_required
def setGroup(attribute_id):
    attr = Attribute.query.get(attribute_id)
    selected_group = request.form.get('select_group')
    if attr.grouping_id != selected_group: 
        attr.grouping_id = selected_group 
        db.session.commit()

    return redirect(url_for("views.admin_view"))


# Group view for listing active groups and adding new ones
@app.route("/801fc3/groups", methods=["GET", "POST"])
@login_required
def group_view():
    if request.method == "GET":
        return render_template("groupView.html", groups=QuestionGroup.query.all())

    form = request.form
    groupname = form.get('group_name')
    groupkey = form.get('group_key')
    fi = form.get('Suomeksi')
    sv = form.get('Svenska')
    en = form.get('English')

    question = '{"fi":"' + fi + '","sv":"' + sv + '","en":"' + en + '"}'
    try:
        json.loads(question)
        db.session.add(QuestionGroup(grouping_key=groupkey,
                                     group_name=groupname, group_question=question))
        db.session.commit()
        return render_template("groupView.html", groups=QuestionGroup.query.all())

    except:
        db.session.rollback()
        return render_template("groupView.html", groups=QuestionGroup.query.all(), error="Item could not be added, this might be due to use of quotes or a duplicate grouping key.")


# Edit Group question
@app.route("/edit_group_question/<group_id>", methods=["GET"])
@login_required
def edit_group_question_view(group_id):
    attribute = QuestionGroup.query.get(group_id)
    json_a = json.loads(attribute.group_question)
    return render_template("langTemplate.html", attribute=json_a, redirect_url=url_for('views.group_view'),
                           post_url=url_for('views.edit_group_question_string', group_id=attribute.id))

# group question edit handler
@app.route("/edit_group_question/<group_id>", methods=["POST"])
@login_required
def edit_group_question_string(group_id):
    group = QuestionGroup.query.get(group_id)

    try:
        form = request.form
        jsoned = json.loads(group.group_question)

        for key in jsoned:
            if(len(form[key]) > 0):
                jsoned[key] = form[key]

        group.group_question = json.dumps(jsoned)
        db.session.commit()
    except:
        print('Data parsing failed in group_question_edit')
        return redirect(url_for("views.group_view", error="Edit failed. This might be caused by quotes in the strings"))

    return redirect(url_for("views.group_view"))

# Edit Group name
@app.route("/edit_group_name/<group_id>", methods=["GET"])
@login_required
def edit_group_name_view(group_id):
    group = QuestionGroup.query.get(group_id)
    string = group.group_name
    return render_template("singleStringEditTemplate.html", string=string, redirect_url=url_for('views.group_view'),
                           post_url=url_for('views.edit_group_name_string', group_id=group.id))

# group name edit handler
@app.route("/edit_group_name/<group_id>", methods=["POST"])
@login_required
def edit_group_name_string(group_id):
    group = QuestionGroup.query.get(group_id)

    try:
        form = request.form
        string = group.group_name
        if len(form.get('string')) > 0:

            group.group_name = form.get('string')
            db.session.commit()
    except:
        print('Data parsing failed in group_name_edit')
        return redirect(url_for("views.group_view", error="Edit failed."))

    return redirect(url_for("views.group_view"))

# Edit Grouping key
@app.route("/edit_group_key/<group_id>", methods=["GET"])
@login_required
def edit_group_key_view(group_id):
    group = QuestionGroup.query.get(group_id)
    string = group.grouping_key
    return render_template("singleStringEditTemplate.html", string=string, redirect_url=url_for('views.group_view'),
                           post_url=url_for('views.edit_group_key', group_id=group.id))

# grouping key edit handler
@app.route("/edit_group_key/<group_id>", methods=["POST"])
@login_required
def edit_group_key(group_id):
    group = QuestionGroup.query.get(group_id)

    try:
        form = request.form
        string = group.grouping_key
        if len(form.get('string')) > 0:

            group.grouping_key = form.get('string')
            db.session.commit()
    except:
        print('Data parsing failed in group_name_edit')
        return redirect(url_for("views.group_view", error="Edit failed."))

    return redirect(url_for("views.group_view"))
