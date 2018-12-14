from project import db
from project.api.models import User

def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def add_admin(username, email, password):
    user = add_user(username=username, email=email, password=password)
    db.session.commit()
    user = User.query.filter_by(username=username).first()
    user.admin=True
    db.session.commit()
    return user
