from datetime import datetime
from oss import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id        =  db.Column(db.Integer, primary_key=True)
    user      =  db.Column(db.String, nullable=True)
    name      =  db.Column(db.String, nullable=False)
    email     =  db.Column(db.String, unique=True, nullable=False)
    password  =  db.Column(db.String(60), nullable=False)
    oss_participated = db.relationship('Oss', backref='participant', lazy=True)
    submissions = db.relationship('Submission', backref="submitter", lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"

class Oss(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String, nullable=False)
    date_posted  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    premise      = db.Column(db.Text, nullable=True)
    challenge    = db.Column(db.Text, nullable=False)
    beginner     = db.Column(db.Text, nullable=True)
    intermediate = db.Column(db.Text, nullable=True)
    advance      = db.Column(db.Text, nullable=False)
    admin_posted = db.Column(db.String, db.ForeignKey('user.name'), nullable=False) #person who posted the OSS
    

    def __repr__(self):
        return f"OSS('{self.title}', '{self.date_posted}')"

class Submission(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String, nullable=True)
    github = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_submitted = db.Column(db.String, db.ForeignKey('user.name'), nullable=False)
    oss_id = db.Column(db.Integer, db.ForeignKey('oss.id'), nullable=False)

