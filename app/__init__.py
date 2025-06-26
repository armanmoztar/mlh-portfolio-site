import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from .data import education

load_dotenv()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        url=os.getenv("URL"),
        education=education  
    )
