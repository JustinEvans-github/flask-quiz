from app import app
import random
from app.tasks import book_page
from app.quiz import *
from wtforms.validators import InputRequired


from flask import render_template, request, redirect, url_for

@app.route('/',methods=['GET','POST'])
def add_task():

    # extract page contents
    page_num = random.randint(0, 40)
    url_start = f'https://books.toscrape.com/catalogue/page-{page_num}.html'

    # define quiz contents
    content = book_page(url_start)
    title_options = [content[0][0],content[1][0],content[2][0]]
    description_answer = content[0][1]
    title_answer = content[0][0]

    # define quiz content in WTForm
    # form = PopQuiz()
    # form.q1.coerce=bool

    # form.q1.choices = [True,'label']#[(True, title_options[0]), (False, title_options[1]),(False,title_options[2])]
    
    # form.q1.validator = [InputRequired()]#[True]#[CorrectAnswer(True)]
    # form.q1.validate_choice = True
    # form.q1.default = True

    # from wtforms import RadioField
    # form.q1 = RadioField(
    # "The answer to question one is False.",
    # choices=[('True', 'True'), ('False', 'False')],
    # validators=[CorrectAnswer('False')]
    # )
    
    form = PopQuiz()
    #form = RadioQuiz()

    if form.is_submitted():
        print ("submitted")
    if form.validate():
        print("validate")

    if form.validate_on_submit():
        print("validated")
        return redirect(url_for('passed'))
    return render_template('add-task.html', form=form, description_answer=description_answer)

    
@app.route('/passed/')
def passed():
    return render_template('passed.html')