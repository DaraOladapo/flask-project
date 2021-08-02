from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

from application.models import Todos


class TodoForm(FlaskForm):
    task = StringField('Task',
        validators = [
            DataRequired(),
        ]    
    )
    submit = SubmitField('Submit')

    def validate_task(self, task):
        todos = Todos.query.all()
        for todo in todos:
            if todo.task == task.data:
                raise ValidationError('You already added this Todo')

class OrderTodo(FlaskForm):
    order_with = SelectField('Order With',
        choices=[
            ("complete", "Completed"),
            ("id", "Recent"),
            ("old", "Old"),
            ('incomplete', "Incomplete")
        ]
    )
    submit = SubmitField('Order')