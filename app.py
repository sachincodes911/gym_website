from datetime import date, datetime
from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import json
import math

#TODO--- final testing before deployment,delete not working


with open("config.json","r") as c:
    params=json.load(c)["params"]

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database/contact.db"
app.config['SECRET_KEY'] = 'herohiralal'    



db=SQLAlchemy(app)



class Contact(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email=db.Column(db.String(30),nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=True)


class Post(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=True)
    category = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(500), nullable=False)




@app.route("/")
def home():
    return render_template("index.html",params=params)


@app.route("/contact",methods=["GET","POST"])
def contact():
    name=request.form.get("name")
    email=request.form.get("email")
    msg=request.form.get("message")
    date=datetime.now().date()
    if request.method=="POST":
        entry=Contact(name=name,email=email,msg=msg,date=date)
        db.session.add(entry)
        db.session.commit()
    
    
    return render_template("contact.html",params=params)

@app.route("/price",methods=["GET","POST"])
def price():
    return render_template("price.html",params=params)


@app.route("/checkout",methods=["GET","POST"])
def checkout():
    if request.method=="POST":
        price=request.form.get("plan")
        print(type(price))
        return(str(price))
    

@app.route("/about")
def about():
    return render_template("about.html",params=params)



@app.route("/service")
def service():
    return render_template("services.html",params=params)


@app.route("/post")
def post():
    page = request.args.get('page', 1, type=int)
    print(page)
    posts=Post.query.all()
    last=math.ceil(len(posts)/params["no_of_page"])
    posts=posts[(int(page)-1)*(int(params['no_of_page'])):(int(page)-1)*(int(params['no_of_page']))+int(params["no_of_page"])]
    if page==1:
        prev="#"
        next=page+1
    elif page==last:
        prev=page-1
        next="#"
    else:
        prev=page-1
        next=page+1
    
    return render_template("post.html",params=params,posts=posts,next=next,prev=prev)


@app.route("/dashboard")
def dashboard():
    posts=Post.query.all()
    if "user" in session and session["user"]==params["user_id"]:
        return render_template("dashboard.html",params=params,posts=posts)
    else:
        return("login to continue")


@app.route("/viewpost/<sno>")
def viewpost(sno):
    post=Post.query.filter_by(sno=sno).first()
    return render_template("viewpost.html",params=params,post=post)

@app.route("/login",methods=["GET","POST"])
def login():
    password=request.form.get("password")
    user_id=request.form.get("user_id")
    if params["user_id"]==user_id and params["password"]==password:
        session['user']=user_id
        return redirect("/dashboard") #render_template("dashboard.html",params=params)
        
    return render_template("login.html",params=params)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html",params=params)


@app.route("/edit/<sno>",methods=["GET","POST"])
def edit(sno):
    if "user" in session and session["user"]==params["user_id"]:
        post=Post.query.filter_by(sno=sno).first()
        if request.method=="POST":
            post.category=request.form.get("category")
            post.title=request.form.get("title")
            post.content=request.form.get("content")
            db.session.commit()
            return redirect("/dashboard")
    return render_template("edit.html",params=params,post=post)


@app.route("/delete/<sno>",methods=["GET","POST"])
def delete(sno):
    if "user" in session and session["user"]==params["user_id"]:
        post=Post.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")

@app.route("/submit",methods=["GET","POST"])
def submit():
    if "user" in session and session["user"]==params["user_id"]:
        if request.method=="POST":
                category=request.form.get("category")
                title=request.form.get("title")
                content=request.form.get("content")
                date=datetime.now().date()
                entry=Post(date=date,category=category,title=title,content=content)
                db.session.add(entry)
                db.session.commit()
                return redirect("/dashboard")


db.create_all()

app.run(debug=True)

