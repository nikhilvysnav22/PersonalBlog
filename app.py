import json
from flask import Flask , render_template ,redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail,Message
from datetime import datetime


with open("config.json",'r' ) as config_file:
    params = json.load(config_file)["params"]

app = Flask(__name__)


app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)

local_server = True

if local_server :
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']

# initialize
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# To Db
class PostTable(db.Model):
    sno = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    date = db.Column(db.DateTime, default= datetime.now())
    name = db.Column(db.String(50), unique=False, nullable=False)
    emailid = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    title = db.Column(db.VARCHAR(500), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
    date = db.Column(db.DateTime, default= datetime.now())
    slug = db.Column(db.VARCHAR(45), unique=False, nullable=False)
    img_file = db.Column(db.VARCHAR(45), unique=False, nullable=False)


@app.route("/")
def home():
    post = Posts.query.filter_by().all()[0:params['blog_display']]
    return render_template('index.html',params = params ,post=post)

@app.route("/homeclick")
def homeclick():
    post = Posts.query.filter_by().all()
    return render_template('index.html',params = params , post=post)

@app.route("/about")
def about():
    return render_template('about.html',params = params)


@app.route("/post/<string:post_slug>" , methods = ['GET','POST'])
def post(post_slug):

    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params = params , post=post)


@app.route("/contact" , methods=['POST', 'GET'])
def contact():
    if request.method == 'POST' :
        # add entry to the database

        name = request.form.get('name')
        emailid = request.form.get('email')
        phone = request.form.get('phone_number')
        message = request.form.get('message')

        entry_to_db = PostTable(name=name, emailid=emailid , phone=phone, message=message)
        db.session.add(entry_to_db)
        db.session.commit()
        msg = Message("Business Question from " + name ,
                      sender=params['gmail-user'],
                      recipients=params['gmail-recipients'] ,
                      body= message + '\n' + phone)
        mail.send(msg)

    return render_template('contact.html',params = params)

if __name__ == '__main__':
    app.run(debug=True, port=4015 , threaded=True)