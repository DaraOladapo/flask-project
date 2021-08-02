from flask import render_template, url_for, redirect, request
from application import app, db
from application.models import Todos
from application.forms import TodoForm, OrderTodo


@app.route('/', methods=['POST', 'GET'])
def index():
    form = OrderTodo()
    totals = {
        "total": Todos.query.count(),
        "total_completed": Todos.query.filter_by(complete=True).count()
    }
    if form.order_with.data == "id":
        todos = Todos.query.order_by(Todos.id.desc()).all()
    elif form.order_with.data == "complete":
        todos = Todos.query.order_by(Todos.complete.desc()).all()
    elif form.order_with.data == "incomplete":
        todos = Todos.query.order_by(Todos.complete).all()
    else:
        todos = Todos.query.all()
    return render_template('index.html', title="Todo List App", todos=todos, form=form, totals=totals)

@app.route('/add', methods=['POST', 'GET'])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todos(
            task = form.task.data,
            complete = False
        )
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', title="Add a new todo", form=form)

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todos.query.get(id)
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/incomplete/<int:id>')
def incomplete(id):
    todo = Todos.query.get(id)
    todo.complete = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = TodoForm()
    todo = Todos.query.get(id)
    if form.validate_on_submit():
        todo.task = form.task.data
        db.session.commit()
        redirect(url_for('index'))
    elif request.method == 'GET':
        form.task.data = todo.task
    return render_template('update.html', title='Update your todo', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todos.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))