from app import app
#from app import r
#from app import q 
import random
from app.tasks import book_page
from app.quiz import PopQuiz, CorrectAnswer

from flask import render_template, request, redirect, url_for


# @app.route('/')
# def index():
#     return "hellow world"

@app.route('/add-task',methods=['GET','POST'])
def add_task():

    # extract page contents
    page_num = random.randint(0, 40)
    url_start = f'https://books.toscrape.com/catalogue/page-{page_num}.html'

    # define quiz contents
    content = book_page(url_start)
    title_options = [content[0][0],content[1][0],content[2][0]]
    description_answer = content[0][1]
    title_answer = [content[0][0]]

    # define quiz content in WTForm
    form = PopQuiz(questions=title_options,answer=title_answer)
    form.question.choices = [('1', title_options[0]), ('2', title_options[1]),('3',title_options[2])]
    form.question.validator = [CorrectAnswer(title_answer)]

    if form.validate_on_submit():
        return redirect(url_for('passed'))
    return render_template('add-task.html', form=form, description_answer=description_answer)

    
@app.route('/passed')
def passed():
    return render_template('passed.html')