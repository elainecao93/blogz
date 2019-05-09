from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hello@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "bronson"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="author_id")

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(4000))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id")

    def __init__(self, title, content, author==None):
        self.title = title
        self.content = content
        self.author_id = author

@app.route("/blog.html")
def blog():
    blog_id = request.args.get("id")
    if blog_id is not None:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", post=post)
    posts = Blog.query.all()
    return render_template("blog.html", posts=posts)

@app.route("/newpost.html", methods=["POST", "GET"])
def newpost():

    title = ""
    content = ""

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if len(title) > 0 and len(content) > 0:
            new_post = Blog(title, content) #TODO add user tag
            db.session.add(new_post)
            db.session.commit()
            return redirect("/blog.html?id="+str(new_post.id))
    
    error = (request.method == "POST")
    return render_template("newpost.html", error=error, title=title, content=content)

@app.route("/login.html", methods=["POST", "GET"])
def login():

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            #TODO flask message for this error
            return render_template("login.html", username="")
        
        if not existing_user.password == password:
            #TODO flash message for this error
            return render_template("login.html" username=username)


    return render_template("login.html", username="")

@app.route("/register.html", methods=["POST", "GET"])
def register():

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            #TODO flask message for this error
            return render_template("register.html", username="")
        
        if len(username) == 0:
            #TODO flash message for this error
            return render_template("register.html", username="")

        if password != verify:
            #TODO flash message for this error
            return render_template("register.html", username=username)
        
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session["username"] = username

        return redirect("/")

    return render_template("register.html", username="")

@app.route("/logoff.html", methods=["GET"])
def logoff():
    del session["username"]
    redirect("/")

@app.route("/blog.html", methods=["GET"]) #TODO fix this nonsense
def blog():
    posts = Blog.query.all()
    return ""

@app.route('/', methods=["POST", "GET"])
def index(): #TODO fix this nonsense
    
    posts = Blog.query.all()

    return render_template("home.html", posts=posts)

@app.before_request()
def validate():
    #TODO

if __name__ == "__main__":
    
    #Make fresh/empty databases each time the program runs, to make it easier to test
    db.drop_all()
    db.create_all()
    db.session.commit()

    app.run()