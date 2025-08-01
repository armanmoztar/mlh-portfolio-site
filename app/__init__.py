import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from .data import education, work_experience, hobbies, visited_places
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict


load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print("Using database:", mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb
        

if not mydb.is_closed():
    mydb.close()
mydb.connect()
mydb.create_tables([TimelinePost], safe=True)


print("MySQL driver:", MySQLDatabase.__module__)

@app.route('/', endpoint='index')
def index():
    return render_template(
        'index.html',
        title="MLH Fellow",
        url=os.getenv("URL"),
        education=education,
        work_experience=work_experience,
        visited_places=visited_places
    )

@app.route("/hobbies", endpoint='hobbies_page')
def hobbies_page():
    return render_template("hobbies.html", title="Hobbies", hobbies=hobbies)

@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    content = request.form.get("content", "").strip()

    if not name:
        return "Invalid name", 400
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return "Invalid email", 400
    if not content:
        return "Invalid content", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route("/api/timeline_posts", methods=["GET"])
def get_time_line_posts():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route("/api/timeline_post/<int:id>", methods=["DELETE"])
def delete_timeline_post(id):
    post = TimelinePost.get_or_none(TimelinePost.id == id)
    if post:
        post.delete_instance()
        return {"message": f"Deleted timeline post with ID {id}"}
    else:
        return {"error": "Post not found"}, 404

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")
