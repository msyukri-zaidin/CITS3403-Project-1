from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app
from app import db
from app.models import Question, CurrentQuestion, QuestionSet, Option, User
from app.forms import QuestionForm, QuestionsetForm, LoginForm, RegistrationForm
import sys
import json
import random
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, QuestionController, QuestionSetController, QuizController

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #If authenticated, redirect to home
        print(current_user.is_active)
        print(current_user.is_anonymous)
        return redirect(url_for('home'))
    #Else, login
    return UserController.login()

@app.route('/logout')
def logout():
    return UserController.logout()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return UserController.register()

@app.route('/', methods = ['GET','POST'])
def home():
    questionSet = QuestionSet.query.all()
    # need to do what happens if the user has laready logged in, would the login button appear differently
    # not too sure on what this success does

    return render_template('home.html', questionSet = questionSet)

@app.route('/quiz', methods = ['GET','POST'])
def generate_quiz():
    return QuizController.generate_quiz()

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    questionset_form = QuestionsetForm()
    form = QuestionForm()
    
    questionsetID = request.args.get('questionsetID')
    #questionsetID will be true only if function was called by questionset()
    if questionsetID:
        questionsetID = int(questionsetID)
    else: 
        questionsetID = 1

    #print(form.errors)

    QuestionController.create_question(form)
    QuestionSetController.create_questionset(questionset_form)


    #These 3 if statements are temporary. Only used when database is initally empty
    """if len(Question.query.all()) == 0:
        q = Question(question = 'What is the capital of Australia', question_type = 'Short-Answer', answer = 'Canberra')
        db.session.add(q)
        db.session.commit()
    if len(CurrentQuestion.query.all()) == 0:
        for i in range(1, 6):
            q = CurrentQuestion(question_id = '', questionset_id = 1, question_number = i)
            db.session.add(q)
        db.session.commit()
    if len(QuestionSet.query.all()) == 0:
        q = QuestionSet(name = 'Test', number_of_questions = 5)
        db.session.add(q)
        db.session.commit()"""


    #Declare variables and initalise them with all values from the tables
    questionPool = Question.query.all()
    #currentQuestion is initialised where the questionsetID is equal to what was previously set
    currentQuestion = CurrentQuestion.query.filter(CurrentQuestion.questionset_id==questionsetID).all()
    questionSet = QuestionSet.query.all()

    #filterList contains all the questions which are in question slots
    #These questions are then filtered out of questionPool
    filterList = []
    filterListLength = Question.query.all()[-1].id
    for i in range(1, filterListLength + 1):
        filterList.append(i)
        
    for cQuestion in currentQuestion:
        for pQuestion in questionPool:
            if cQuestion.question_id == pQuestion.id:
                #print(cQuestion.question_id) #To check what question IDs are in question slots
                filterList.remove(cQuestion.question_id)

    #The line where filtering occurs
    questionPool = Question.query.filter(Question.id.in_(filterList)).all()

    questionset_number_of_questions = QuestionSet.query.filter_by(id=questionsetID).first().number_of_questions
    return render_template(
        'admin_page.html', 
        questionPool = questionPool, 
        questionset_form = questionset_form, 
        form = form,
        currentQuestion = currentQuestion, 
        questionSet = questionSet, 
        currentSet = QuestionSet.query.filter_by(id=questionsetID).first(),                         #ID deducted by 1 to get position
        questionSetNumberOfQuestions = questionset_number_of_questions, #Number of questions in the question set
        questionSetTotal = len(questionSet))                            #Total number of question sets

#Test function
@app.route('/base')
def base():

    #return render_template('base.html')
    return redirect(url_for('admin', questionsetID = 2))

#Function that is initiated by an AJAX call that comes from saving changes to the question arrangement
@app.route('/postquestion', methods = ['POST'])
def get_question_data():
    return QuestionController.question_arrangement()

#INCOMPLETE: Function for deleting a question
@app.route('/deletequestion', methods = ['POST'])
def delete_question():
    return QuestionController.delete_question()

#Function that is initiated by an AJAX call that comes from selecting a new question set from the dropdown menu
#Function switches the active question set to the selected set
@app.route('/loadquestionset', methods = ['GET','POST'])
def questionset():
    setDict = request.get_json(force=True)
    questionsetID = setDict['questionsetID']
    return redirect(url_for('admin', questionsetID = questionsetID))

#Function that is initiated by an AJAX call that comes from editing a question
@app.route('/editquestion', methods= ['POST'])
def edit_question():
    return QuestionController.edit_question()

#Function that is initiated by an AJAX call that comes from deleting a question set
@app.route('/deleteset', methods=['POST'])
def delete_set():
    return QuestionSetController.delete_questionset()