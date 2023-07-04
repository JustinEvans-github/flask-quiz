from app import app
import random
from app.tasks import book_page
from app.quiz import *
from wtforms.validators import InputRequired


from nltk.tokenize import sent_tokenize

from flask import render_template, request, redirect, url_for, flash

@app.route('/',methods=['GET','POST'])
def base():
    return render_template('base.html')

@app.route('/webscrape',methods=['GET','POST'])
def webscrape():
    # extract page contents
    page_num = random.randint(0, 40)
    url_start = f'https://books.toscrape.com/catalogue/page-{page_num}.html'

    # define quiz contents
    content = book_page(url_start)
    global title_options
    title_options = [content[0][0],content[1][0],content[2][0]]
    print(f'Answer: {content[0][0]}')

    description_answer_all = content[0][1]

    # extract first three sentences
    global description_answer
    description_answer = ' '.join(sent_tokenize(description_answer_all)[0:2])

    return redirect(url_for('quiz'))

@app.route('/quiz',methods=['GET','POST'])
def quiz():

    # define quiz content in WTForm
    #form = PopQuiz()
    form = RadioQuiz()
    form.q1.choices = [('False', title_options[0]), ('True', title_options[1]),(False,title_options[2])]
    form.q1.validator = [CorrectAnswer('False')]

    if form.is_submitted():
        print ("submitted")
        print(form.errors)
    if form.validate():
        print("validate")
        print(f'form.data {form.data}')

    if form.validate_on_submit():
        print("validated on submit")
        return redirect(url_for('quiz'))
    return render_template('quiz.html', form=form, description_answer=description_answer)

    
@app.route('/passed/')
def passed():
    flash('Correct Answer')
    return render_template('passed.html', form=form, description_answer=description_answer)