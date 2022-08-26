from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'FISH'

toolbar = DebugToolbarExtension(app)

# ----------

responses = []


@app.route("/")
def home_page():
    responses.clear()
    return render_template("home.html", survey=satisfaction_survey)


@app.route("/questions/<number>")
def questions_page(number):

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")

    if (int(number) - 1 != len(responses)):
        flash("Nice try!")
        return redirect(f"/questions/{len(responses) + 1}")

    question = satisfaction_survey.questions[int(number) - 1].question
    choices = satisfaction_survey.questions[int(number) - 1].choices

    return render_template("questions.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def answer_page():
    responses.append(request.form["choice"])
    return redirect(f"/questions/{len(responses) + 1}")


@app.route("/complete")
def complete_page():
    return render_template("complete.html", responses=responses)
