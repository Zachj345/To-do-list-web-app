from flask import Flask
from flask import render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

time = datetime.datetime.now().strftime('%m-%d-%Y, %I:%M %p %Z%z')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class DataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    task = db.Column(db.String(400), nullable=False)


@app.route('/')
def home():
    return render_template('idx.html', time=time)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    task = request.form.get('task')
    new_item = DataBase(name=name, task=task)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:id>')
def delete(id):
    todo = DataBase.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('item_list'))


@app.route('/list/')
def item_list():
    lst = DataBase.query.all()
    return render_template('items.html', lst=lst)


if __name__ == '__main__':
    app.run(debug=True)
