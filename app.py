# from crypt import methods
from email.policy import default
from unicodedata import name
from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)
    # return 'Hello, World!'

@app.route('/about')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    # return 'This is about page.'
    return render_template('about.html', allTodo = allTodo)

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    tobe_updated_item = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo = tobe_updated_item)

@app.route('/delete/<int:sno>')
def delete(sno):
    tobe_deleted_item = Todo.query.filter_by(sno=sno).first()
    db.session.delete(tobe_deleted_item)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=8000)