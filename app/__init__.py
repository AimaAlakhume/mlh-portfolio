import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from datetime import *
from playhouse.shortcuts import model_to_dict

class Person:
    def __init__(self, f_name, l_name, school, major, hob1, hob2, hob3, hob4):
        self.f_name = f_name
        self.l_name = l_name
        self.school = school
        self.major = major
        self.hob1 = hob1
        self.hob2 = hob2
        self.hob3 = hob3
        self.hob4 = hob4



load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306)

print(mydb)


sristi = Person("Sristi", "Panchu", "Tufts University", "Computer Science", "crafting (specifically quilling)", "dancing", "reading", "exploring new places")
aima = Person("Aima", "Alakhume", "New York University", "Electrical Engineering", "painting", "writing", "reading", "exploring new places")

@app.route('/')
def index():
    return render_template('index.html', title="Our Portfolios", url=os.getenv("URL"))

@app.route('/aima')
def abaima():
    return render_template('aboutaima.html', student = aima)

@app.route('/sristi')
def absristi():
    return render_template('aboutsristi.html', student = sristi)



class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])


#POST route
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


#GET endpoint
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


#timeline page
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title='Timeline')

