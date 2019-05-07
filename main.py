from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:beproductive@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    text = db.Column(db.String(4000))

    def __init__(self, title, text=""):
        self.title = title
        self.text = text

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        new_post = Blog(title, text)
        db.session.add(new_post)
        db.session.commit()
    
    posts = Blog.query.all()

    return render_template("home.html", posts=posts)

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    db.session.commit()

    app.run()