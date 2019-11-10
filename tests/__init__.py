def init_test_db(app):
    from src.models import db, Answer, AnswerQuestion, Attribute, BuildingClass, Session

    with app.app_context():
        # Clear all tables
        [db.session.remove(x) for x in Answer.query.all()]
        [db.session.remove(x) for x in AnswerQuestion.query.all()]
        [db.session.remove(x) for x in Attribute.query.all()]
        [db.session.remove(x) for x in BuildingClass.query.all()]
        [db.session.remove(x) for x in Session.query.all()]

        # Initialize attribute table
        db.session.add(Attribute(attribute_id='1',
                                 attribute_name='Asunnot',
                                 attribute_question='Onko rakennuksessa asunnot?'))
        db.session.add(Attribute(attribute_id='101',
                                 attribute_name='Asuinhuone',
                                 attribute_question='Onko rakennuksessa asuinhuone?'))
        db.session.add(Attribute(attribute_id='102',
                                 attribute_name='Eteinen',
                                 attribute_question='Onko rakennuksessa eteinen?'))

        # Initialize building_classes table
        db.session.add(BuildingClass(class_id='0110',
                                     class_name='Omakotitalot'))
        db.session.add(BuildingClass(class_id='0111',
                                     class_name='Paritalot'))
        db.session.add(BuildingClass(class_id='0112',
                                     class_name='Rivitalot'))

        # Initialize answer table
        db.session.add(Answer(value='yes'))
        db.session.add(Answer(value='no'))
        db.session.add(Answer(value='skip'))

        # Commit initialization
        db.session.commit()
