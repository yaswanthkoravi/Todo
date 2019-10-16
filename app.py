from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200),nullable=False)
    complete = db.Column(db.Boolean,default=False)
@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html', incomplete=incomplete, complete=complete)

@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/c_clear')
def C_clear_task():
    task = Todo.query.filter_by(complete=True).all()
    for i in task:
        db.session.delete(i)
    db.session.commit()
    return redirect('/')
@app.route('/i_clear')
def I_clear_task():
    task = Todo.query.filter_by(complete=False).all()
    for i in task:
        db.session.delete(i)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
