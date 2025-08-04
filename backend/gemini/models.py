from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

class TrackedProduct(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    category=db.Column(db.String(50))
    color=db.Column(db.String(50))
    size=db.Column(db.String(50))
    gender=db.Column(db.String(50))
    features=db.Column(db.String(50))

    name = db.Column(db.String(255))
    price = db.Column(db.String(50))
    link = db.Column(db.String(255))
