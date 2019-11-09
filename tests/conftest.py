from src import create_app
from config import TestingConfig
from src.models import Session, AnswerQuestion
import pytest

@pytest.fixture(scope='module')
def backend():
    app = create_app(TestingConfig)

    test_client = app.test_client()

    ctxt = app.app_context()
    ctxt.push()

    yield test_client

    Session.query.delete()
    AnswerQuestion.query.delete()

    ctxt.pop()
