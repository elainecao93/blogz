from flask import Flask, request, redirect, render_template, session, flash
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
    blogs = db.relationship("Blog", backref="author")

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(4000))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author_id = author

@app.route("/blog.html")
def blog():
    blog_id = request.args.get("id")
    if blog_id is not None:
        post = Blog.query.filter_by(id=blog_id).first()
        return render_template("post.html", post=post)
    user_id = request.args.get("user")
    if user_id is not None:
        author = User.query.filter_by(id=user_id).first()
        posts = Blog.query.filter_by(author_id=user_id).all()
        return render_template("singleuser.html", author=author.username, posts=posts)
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
            username = session["username"]
            user = User.query.filter_by(username=username).first()
            if not user:
                #TODO fix this error (though it shouldn't exist?)
                ""
            new_post = Blog(title, content, user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect("/blog.html?id="+str(new_post.id))
    
    if request.method == "POST":
        flash("You must enter something not blank for both the title and the blog content.")
    return render_template("newpost.html", title=title, content=content)

@app.route("/login.html", methods=["POST", "GET"])
def login():

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            flash("Username doesn't match a registered user.")
            return render_template("login.html", username="")
        
        if not existing_user.password == password:
            flash("Password is incorrect.")
            return render_template("login.html", username=username)


    return render_template("login.html", username="")

@app.route("/register.html", methods=["POST", "GET"])
def register():

    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        verify = request.form["verify"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("That username already exists.")
            return render_template("register.html", username="")
        
        if len(username) == 0:
            flash("Your undername can't be blank.")
            return render_template("register.html", username="")

        if password != verify:
            flash("Your password fields don't match.")
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
    return redirect("/")

@app.route('/', methods=["POST", "GET"])
def index(): #TODO fix this nonsense
    
    users = User.query.all()

    return render_template("home.html", users=users)

@app.before_request
def validate():
    if "email" not in session and request.endpoint == "/newpost.html":
        return redirect("/login.html")

if __name__ == "__main__":
    
    #Make fresh/empty databases each time the program runs, to make it easier to test
    db.drop_all()
    db.create_all()
    db.session.commit()

    app.run()