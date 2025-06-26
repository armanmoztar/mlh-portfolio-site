import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from .data import education, work_experience, hobbies

load_dotenv()
app = Flask(__name__)


@app.route('/', endpoint='index')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        url=os.getenv("URL"),
        education=education,
        work_experience=work_experience,
    )

@app.route("/hobbies", endpoint='hobbies_page')
def hobbies_page():
    return render_template("hobbies.html", title="Hobbies", hobbies=hobbies)
