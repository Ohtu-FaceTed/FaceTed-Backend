def init_test_db(app):
    from src.models import db, Answer, AnswerQuestion, Attribute, BuildingClass, Session, QuestionGroup

    with app.app_context():
        # Clear all tables
        [db.session.remove(x) for x in Answer.query.all()]
        [db.session.remove(x) for x in AnswerQuestion.query.all()]
        [db.session.remove(x) for x in Attribute.query.all()]
        [db.session.remove(x) for x in BuildingClass.query.all()]
        [db.session.remove(x) for x in Session.query.all()]

        # Initialize question_group table
        db.session.add(QuestionGroup(grouping_key='1',
                                     group_name='WC:t',
                                     group_question='Minkälaisia WC-tiloja rakennuksessa on?'))

        # Initialize attribute table
        db.session.add(Attribute(attribute_id='1',
                                 attribute_name='Asunnot',
                                 attribute_question='Onko rakennuksessa asunnot?',
                                 grouping_id=None,
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='101',
                                 attribute_name='Asuinhuone',
                                 attribute_question='Onko rakennuksessa asuinhuone?',
                                 grouping_id=None,
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='102',
                                 attribute_name='Eteinen',
                                 attribute_question='Onko rakennuksessa eteinen?',
                                 grouping_id=None,
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='114',
                                 attribute_name='WC',
                                 attribute_question='Onko rakennuksessa WC?',
                                 grouping_id='1',
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='116',
                                 attribute_name='WC-pesuhuone',
                                 attribute_question='Onko rakennuksessa WC-pesuhuone?',
                                 grouping_id='1',
                                 active=True,
                                 attribute_tooltip=''))

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
