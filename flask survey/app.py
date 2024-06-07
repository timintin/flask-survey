from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses"

@app.route('/')
def show_survey_start():
    return render_template('survey_start.html', survey=satisfaction_survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)

@app.route('/answer', methods=["POST"])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def complete():
    return render_template('completion.html')

if __name__ == "__main__":
    app.run(debug=True)
