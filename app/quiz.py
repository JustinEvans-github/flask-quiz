from flask_wtf import FlaskForm as Form
from wtforms import RadioField
from wtforms.validators import ValidationError
from random import randrange

# source: https://github.com/adityachandavale/flask-wt-forms-example/blob/main/quiz.py
class CorrectAnswer(object):
    def __init__(self, answer):
        self.answer = answer

    def __call__(self, form, field):
        message = 'Incorrect answer.'

        if field.data != self.answer:
            raise ValidationError(message)


class PopQuiz(Form):
    class Meta:
        csrf = False

    question = RadioField() # values set in 'views.py'

