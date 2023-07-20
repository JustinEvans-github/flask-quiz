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

    # randomize quiz and re-find 'false' flag
    global title_options
    title_options = [('True',content[0][0]),('True',content[1][0]),('False',content[2][0])]
    random.shuffle(title_options)

    title_answer = [x for x in title_options if "False" in x][0][1]
    description_answer_all = [x for x in content if title_answer in x][0][1]
    
    global url_answer
    url_answer = [x for x in content if title_answer in x][0][2]
    
    # extract first three sentences
    global description_answer
    description_answer = ' '.join(sent_tokenize(description_answer_all)[0:2])

    print(f'Title Answer: {title_answer}')
    print(f'Description Answer: {description_answer}')

    return redirect(url_for('quiz'))

@app.route('/quiz',methods=['GET','POST'])
def quiz():

    # define quiz content in WTForm
    form = RadioQuiz()
    form.q1.choices = title_options
    form.q1.validator = [CorrectAnswer('False')]

    if form.is_submitted():
        print ("submitted")
        print(form.errors)
    if form.validate():
        print("validate")
        print(f'form.data {form.data}')

    if form.validate_on_submit():
        return redirect(url_for('passed'))
    
    if request.method == 'POST' and not form.validate_on_submit():
        return redirect(url_for('failed'))
    return render_template('quiz.html', form=form, description_answer=description_answer, url_answer=url_answer)

# TODO: cleanup unnecessary duplication w/ form inputs    
@app.route('/passed/')
def passed():
    # define quiz content in WTForm
    form = RadioQuiz()
    form.q1.choices = title_options
    form.q1.validator = [CorrectAnswer('False')]

    flash('Correct Answer!')
    return render_template('passed.html', form=form, description_answer=description_answer, url_answer=url_answer)

@app.route('/failed/')
def failed():
    # define quiz content in WTForm
    form = RadioQuiz()
    form.q1.choices = title_options
    form.q1.validator = [CorrectAnswer('False')]

    flash('Wrong title. Try again!')
    return render_template('failed.html', form=form, description_answer=description_answer, url_answer=url_answer)