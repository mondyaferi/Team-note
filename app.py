from flask import render_template, redirect, Flask, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from werkseug import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "postgresql://@localhost/sports"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "MONDY123"


db = SQLAlchemy(app)
Migrate(app, db)

class Makeform(FlaskForm):
      reason = StringField("whats on your mind", validators=[DataRequired()])      
      submit = SubmitField("save")
   

class Name(db.Model):
    __tablename__ = "names"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    
    # Establishes relationship to Excuse model
    excuses = db.relationship('Excuse', backref='name', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    @property 
     def password ():
       raise AttributeError("password not meet requirment")

    @password
    def password (self.password):
      passowrd=generate_password_hash(self.password)    

     @password
     def verify_password(self.password, password )

class Excuse(db.Model):
    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Text, nullable=True)
    
    # Must point to 'names.id' (matching __tablename__ = "names")
    name_id = db.Column(db.Integer, db.ForeignKey('names.id'))

    def __init__(self, reason, name_id):
        self.reason = reason
        self.name_id = name_id



@app.route("/")
def host():
    return redirect (url_for("login"))

@app.route("/home")
def home():
    table = Name.query.all()
    return render_template("root.html", table=table)

@app.route("/form")
def form():
    table = Name.query.all()

    return  render_template("form.html", table=table)

@app.route("/index/<int:id>")
def index(id):
     
    item = db.session.get(Name, id)
    db.session.commit() 
    return render_template("edit.html", item=item)

@app.route("/add/<int:df>", methods=["GET", "POST"])
def add (df ):

    if request.method == "POST":
        if df==0:
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            new=Name(firstname, lastname)
            db.session.add(new)
            db.session.commit()
            return redirect( url_for("add", df=0))
        else :
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            new=Name(firstname, lastname)

            chg=Name.query.get(df)
            chg.firstname= firstname
            chg.lastname= lastname
            db.session.add(chg)
            db.session.commit()
            return redirect( url_for("form"))

    return render_template("new.html")
#delet a name
@app.route("/delete/<int:id>")
def delete(id):
    item=db.session.get(Name, id)
    db.session.delete(item)
    db.session.commit()
    return  redirect(url_for("form"))

#login route
@app.route("/login",  methods=["GET",  "POST"])
def login():
    if request.method == "POST":
       username = request.form["username"]
       passward = request.form["passward"]
       if username == "admin" and passward == "pass":
           return redirect(url_for("home"))
       else:
           return  render_template( "login.html", status="status")

    return render_template( "login.html")

#see all  post/excuse of a user
@app.route("/exc/<int:user>", methods=["GET", "POST"])
def make(user):
    
    student = Name.query.get(user)
    res=student.excuses.all()
    return render_template("reasons.html", res=res, user=user, form=form)

#make a new post/reason for a user
@app.route("/exc/<int:user>/mang", methods=["GET", "POST"])
def excd(user):
    form = Makeform()
    if request.method =="POST":
        if form.validate_on_submit():    
            reason = form.reason.data
            db.session.add(Excuse(reason, user))
            db.session.commit()
            flash ("you got it")
            return  redirect(url_for("make", user=user))
        print (form.errors)
    return  render_template("make.html", user=user, form=form)

# see all post feeds
@app.route("/allexcuses")
def allexc():
  excall = Excuse.query.all()
  return render_template("allexc.html", excall=excall )

#delete an Excuse post/reason
@app.route("/exc/delete/<int:excid>/<int:user>")
def excdel(excid, user):
#    if request.method == "POST":           
    exid=db.session.get(Excuse, excid)
    db.session.delete(exid)
    db.session.commit()
    return redirect(url_for("make", user=user))
  
if __name__== "__main__":
    app.run (debug=False)

