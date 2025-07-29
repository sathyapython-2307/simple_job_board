from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))

@app.route('/')
def home():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/post', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job = Job(
            title=request.form['title'],
            description=request.form['description'],
            location=request.form['location']
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)