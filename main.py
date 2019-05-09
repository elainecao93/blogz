from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:hello@localhost:8889/blogz'
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
            new_post = Blog(title, content)
            db.session.add(new_post)
            db.session.commit()
            return redirect("/blog.html?id="+str(new_post.id))
    
    error = (request.method == "POST")
    return render_template("newpost.html", error=error, title=title, content=content)

@app.route('/', methods=["POST", "GET"])
def index():
    
    posts = Blog.query.all()

    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    
    #Make fresh/empty databases each time the program runs, to make it easier to test
    db.drop_all()
    db.create_all()
    db.session.commit()

    if (True): #basic test cases. Set to false when running
        db.session.add(Blog("sample title 1", "sample text 1"))
        db.session.commit()
        db.session.add(Blog("sample title 2", "sample text 2. The quick brown fox jumps over the lazy dog."))
        db.session.commit()

    app.run()