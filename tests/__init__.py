def init_test_db(app):
    from src import building_data
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
                                     group_question='{"fi":"Minkälaisia WC-tiloja rakennuksessa on?", "sv":"[Svenska]Hurudana toaletter innehåller byggnaden?", "en":"[English]What kinds of restrooms does the space contain?"}'))

        # Initialize attribute table
        db.session.add(Attribute(attribute_id='1',
                                 attribute_name='{"fi":"Asunnot", "sv":"[Svenska]Asunnot", "en":"[English]Asunnot"}',
                                 attribute_question='{"fi":"Onko rakennuksessa asunnot?", "sv":"[Svenska]Onko rakennuksessa asunnot?", "en":"[English]Onko rakennuksessa asunnot?"}',
                                 grouping_id=None,
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='101',
                                 attribute_name='{"fi":"Asuinhuone", "sv":"[Svenska]Asuinhuone", "en":"[English]Asuinhuone"}',
                                 attribute_question='{"fi":"Onko rakennuksessa asuinhuone?", "sv":"[Svenska]Onko rakennuksessa asuinhuone?", "en":"[English]Onko rakennuksessa asuinhuone?"}',
                                 grouping_id=None,
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='102',
                                 attribute_name='{"fi":"Eteinen", "sv":"[Svenska]Eteinen", "en":"[English]Eteinen"}',
                                 attribute_question='{"fi":"Onko rakennuksessa eteinen?", "sv":"[Svenska]Onko rakennuksessa eteinen?", "en":"[English]Onko rakennuksessa eteinen?"}',
                                 grouping_id=None,
                                 active=True,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='114',
                                 attribute_name='{"fi":"WC", "sv":"[Svenska]WC", "en":"[English]WC"}',
                                 attribute_question='{"fi":"Onko rakennuksessa wc?", "sv":"[Svenska]Onko rakennuksessa wc?", "en":"[English]Onko rakennuksessa wc?"}',
                                 grouping_id='1',
                                 active=False,
                                 attribute_tooltip=''))
        db.session.add(Attribute(attribute_id='116',
                                 attribute_name='{"fi":"WC-pesuhuone", "sv":"[Svenska]WC-pesuhuone", "en":"[English]WC-pesuhuone"}',
                                 attribute_question='{"fi":"Onko rakennuksessa wc-pesuhuone?", "sv":"[Svenska]Onko rakennuksessa wc-pesuhuone?", "en":"[English]Onko rakennuksessa wc-pesuhuone?"}',
                                 grouping_id='1',
                                 active=False,
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

        # Refresh building data cache
        building_data.load_from_db()


def init_classifier():
    import numpy as np
    import pandas as pd
    from src import classifier
    from src.naive_bayes_classifier import calculate_conditional_probabilities

    # Add obseravations for all the attributes we define in the test database
    observations = pd.DataFrame({'class_id': ['0110', '0111', '0112'],
                                 'count': [1, 1, 1],
                                 '1': [1, 1, 1],
                                 '101': [1, 1, 0],
                                 '102': [1, 0, 1],
                                 '114': [0, 1, 1],
                                 '116': [1, 0, 0]})

    # Generate the conditional probability table
    classifier.conditional_probabilities = calculate_conditional_probabilities(
        observations)

    # Initialize the prior
    classifier.prior = np.ones(3)

    return classifier
