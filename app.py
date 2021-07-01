import json,os
from flask import Flask , render_template ,redirect, url_for, request , session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail,Message
from datetime import datetime
from werkzeug.utils import secure_filename


with open("config.json",'r' ) as config_file:
    params = json.load(config_file)["params"]

app = Flask(__name__)
app.config['file_location'] = params['file_location']

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

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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
    return render_template('about.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET', 'POST'])
def post(post_slug) :
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)

@app.route("/upload", methods=['GET', 'POST'])
def upload() :
    if ('user' in session) and (session['user'] == params['login_email']) :
        if request.method == ['POST']:
            f = request.files['filename']
            f.save(os.path.join(app.config['file_location']),secure_filename(f.filename))
    return "File uploaded"

@app.route("/logout", methods=['GET', 'POST'])
def logout() :
    if ('user' in session) and (session['user'] == params['login_email']) :
            session.pop('user')
            return redirect('/dashboard')

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

@app.route("/dashboard" , methods=['GET','POST'])
def dashboard():
        post = Posts.query.filter_by().all()[0 :params['blog_display']]

        if ('user' in session) and (session['user'] == params['login_email']):
            return render_template('after_login.html',params = params , post=post)

        if request.method == 'POST' :
            username = request.form.get('uemail')
            userpassword = request.form.get('upassword')
            if (username == params['login_email']) and (userpassword == params['login_password']):
                session['user'] = username
                return render_template('after_login.html',params=params , post=post)

        return render_template('dashboard.html',params = params)

@app.route("/edit/<string:sno>" , methods=['GET','POST'])
def edit(sno):
    if ('user' in session) and (session['user'] == params['login_email']) :
        if request.method == 'POST' :
            title = request.form.get('title')
            slug = request.form.get('slug')
            content_name = request.form.get('content_name')
            image_name = request.form.get('image_name')
            date_time = datetime.now()

            if sno == '0':
                edit_posts = Posts(title=title, content=content_name, date=date_time, slug=slug , img_file=image_name)
                db.session.add(edit_posts)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = title
                post.content = content_name
                post.date = date_time
                post.slug = slug
                post.img_file = image_name
                db.session.commit()

                print(content_name)
                return redirect("/edit/"+sno)

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit_post.html',params = params ,post =post , sno=sno)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, port=4015 , threaded=True)