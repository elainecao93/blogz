from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hello@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(4000))

    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route("/blog.html")
def blog():
    posts = Blog.query.all()
    return render_template("blog.html", posts=posts)

@app.route("/newpost.html", methods=["POST", "GET"])
def newpost():

    title = ""
    text = ""

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if len(title) > 0 and len(text) > 0:
            new_post = Blog(title, content)
            db.session.add(new_post)
            db.session.commit()
            redirect("/") #TODO

    error = not (request.args.get("error") is None)
    return render_template("newpost.html", error=error, title=title, text=text)

@app.route('/', methods=["POST", "GET"])
def index():
    
    posts = Blog.query.all()

    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    db.session.commit()

    app.run()