from flask import Flask , render_template ,redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Discover123!@localhost/blog'

# initialize
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# To Db
class PostTable(db.Model):
    sno = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    date = db.Column(db.DateTime, default= datetime.now())
    name = db.Column(db.String(120), unique=False, nullable=False)
    emailid = db.Column(db.String(50), unique=False, nullable=False)
    phone = db.Column(db.String(15), unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/homeclick")
def homeclick():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post")
def post():
    return render_template('post.html')

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
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=4015 , threaded=True)
