from application import db

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    task = db.Column(db.String(30), unique=True)

    complete = db.Column(db.Boolean, default=False)