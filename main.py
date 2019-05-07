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

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Blog(title, content)
        db.session.add(new_post)
        db.session.commit()
    
    posts = Blog.query.all()

    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    db.session.commit()

    app.run()